import csv
import io
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import TestCase
from .serializers import TestCaseSerializer, TestCaseCreateUpdateSerializer

User = get_user_model()


# 导入导出安全相关限制
MAX_IMPORT_SIZE = 2 * 1024 * 1024  # 2MB
MAX_IMPORT_ROWS = 5000
CSV_HEADER = [
    'product',
    'module',
    'sub_module',
    'test_point',
    'title',
    'description',
    'precondition',
    'steps',
    'expected_result',
    'actual_result',
    'priority',
    'status',
    'stage',
    'case_type',
    'remark',
]


def sanitize_csv_cell(value: str) -> str:
    """
    导出时对单元格做简单安全处理：
    - 若以 =,+,-,@ 开头，前面加单引号，避免被 Excel 当成公式执行
    """
    if not value:
        return ''
    v = str(value)
    if v and v[0] in ('=', '+', '-', '@'):
        return "'" + v
    return v


class TestCasePagination(PageNumberPagination):
    """分页设置：支持 ?page=1&limit=20"""
    page_query_param = 'page'
    page_size_query_param = 'limit'
    page_size = 20
    max_page_size = 200


class TestCaseViewSet(viewsets.ModelViewSet):
    """
    测试用例 CRUD API
    - list:   GET    /api/testcases/         列表（支持分页 + 筛选）
    - create: POST   /api/testcases/         新建
    - retrieve: GET  /api/testcases/{id}/    详情
    - update: PUT    /api/testcases/{id}/    全量更新
    - partial_update: PATCH /api/testcases/{id}/  部分更新
    - destroy: DELETE /api/testcases/{id}/  删除

    分页参数：
    - page:  第几页，从 1 开始
    - limit: 每页条数（默认 20）

    筛选参数（全部可选）：
    - product      产品
    - module       功能模块
    - sub_module   子模块
    - test_point   测试点
    - priority     优先级：low/medium/high/critical
    - status       状态：draft/active/deprecated/closed
    - stage        阶段：smoke/pre_prod/production
    - case_type    用例类型
    - keyword      关键字（在 title / description / test_point 中模糊搜索）
    """

    queryset = TestCase.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = TestCasePagination
    # 对外主 ID 使用雪花 public_id，URL 为 /api/testcases/<public_id>/
    lookup_field = 'public_id'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        """支持简单的查询筛选"""
        qs = super().get_queryset()
        params = self.request.query_params

        # 精确字段筛选
        product = params.get('product')
        module = params.get('module')
        sub_module = params.get('sub_module')
        test_point = params.get('test_point')
        priority = params.get('priority')
        status_param = params.get('status')
        case_type = params.get('case_type')
        stage = params.get('stage')

        if product:
            qs = qs.filter(product__icontains=product)
        if module:
            qs = qs.filter(module__icontains=module)
        if sub_module:
            qs = qs.filter(sub_module__icontains=sub_module)
        if test_point:
            qs = qs.filter(test_point__icontains=test_point)
        if priority:
            qs = qs.filter(priority=priority)
        if status_param:
            qs = qs.filter(status=status_param)
        if case_type:
            qs = qs.filter(case_type__icontains=case_type)

        if stage:
            qs = qs.filter(stage=stage)

        # 严重程度筛选
        severity = params.get('severity')
        if severity:
            qs = qs.filter(severity=severity)

        # 指派人员筛选
        assignee = params.get('assignee')
        if assignee:
            qs = qs.filter(assignee_id=assignee)

        # 只看我的指派
        my_assigned = params.get('my_assigned')
        if my_assigned in ('true', '1'):
            qs = qs.filter(assignee=self.request.user)

        # 关键字搜索
        keyword = params.get('keyword')
        if keyword:
            from django.db.models import Q
            qs = qs.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(test_point__icontains=keyword)
            )

        return qs

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TestCaseCreateUpdateSerializer
        return TestCaseSerializer

    def perform_create(self, serializer):
        # 若已登录，自动关联当前用户为创建人
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(creator=user, updater=user)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        # 返回完整序列化数据
        output = TestCaseSerializer(instance).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        old_assignee_id = instance.assignee_id
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(updater=user)
        else:
            serializer.save()
        instance.refresh_from_db()

        # 指派人员变更时发送通知
        new_assignee = instance.assignee
        if new_assignee and new_assignee.id != old_assignee_id:
            self._send_assignment_notification(instance, new_assignee, request.user)

        output = TestCaseSerializer(instance).data
        return Response(output)

    def _send_assignment_notification(self, testcase, assignee, assigner):
        """发送指派通知（站内消息）"""
        # TODO: 集成站内消息系统后在此处发送通知
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[指派通知] 用例「{testcase.title}」已由 {assigner.nickname} 指派给 {assignee.nickname}")

    @action(detail=False, methods=['get'], url_path='users')
    def users(self, request):
        """获取可指派的用户列表（排除admin）"""
        users = User.objects.exclude(username='admin').values('id', 'nickname', 'username')
        return Response(list(users))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ------- 表格导出 / 导入 / 模板 -------

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        """
        导出用例为 CSV 表格
        - 若提供 ids 参数：仅导出勾选的用例（ids 为 public_id，逗号分隔）
          GET /api/testcases/export/?ids=195707894033010688,195707894033010689
        - 否则：导出当前筛选条件下的全部用例
          GET /api/testcases/export/?product=...&module=...
        """
        queryset = self.get_queryset()

        # 支持按勾选 ID 导出：ids=1,2,3
        ids_param = request.query_params.get('ids')
        if ids_param:
            try:
                raw_ids = [x.strip() for x in ids_param.split(',') if x.strip()]
                # 限制最多一次导出 1000 条，防止恶意传超长列表
                if len(raw_ids) > 1000:
                    return Response(
                        {'code': 40000, 'error': '一次最多导出 1000 条，请缩小勾选范围'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                id_list = [int(x) for x in raw_ids]
            except ValueError:
                return Response({'code': 40000, 'error': 'ids 参数格式错误，应为逗号分隔的 public_id（数字）'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(public_id__in=id_list)

        # 定义导出列（与导入模板保持一致）
        header = CSV_HEADER

        def bool_to_str(v):
            return '1' if v else '0'

        # 使用内存缓冲区生成 CSV（带 BOM，兼容 Excel）
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)

        for tc in queryset:
            writer.writerow([
                sanitize_csv_cell(tc.product or ''),
                sanitize_csv_cell(tc.module or ''),
                sanitize_csv_cell(tc.sub_module or ''),
                sanitize_csv_cell(tc.test_point or ''),
                sanitize_csv_cell(tc.title or ''),
                sanitize_csv_cell(tc.description or ''),
                sanitize_csv_cell(tc.precondition or ''),
                sanitize_csv_cell(tc.steps or ''),
                sanitize_csv_cell(tc.expected_result or ''),
                sanitize_csv_cell(tc.actual_result or ''),
                tc.priority or '',
                tc.status or '',
                tc.stage or '',
                sanitize_csv_cell(tc.case_type or ''),
                sanitize_csv_cell(tc.remark or ''),
            ])

        csv_content = buffer.getvalue()
        buffer.close()

        # 添加 UTF-8 BOM，避免 Excel 中文乱码
        csv_bytes = ('﻿' + csv_content).encode('utf-8')

        filename = f'testcases_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        resp = HttpResponse(csv_bytes, content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = f'attachment; filename="{filename}"'
        return resp

    @action(detail=False, methods=['get'], url_path='template')
    def template(self, request):
        """
        下载导入模板（仅表头一行）
        GET /api/testcases/template/
        """
        # 使用统一表头常量，避免导入导出不一致
        header = CSV_HEADER

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)
        csv_content = buffer.getvalue()
        buffer.close()

        csv_bytes = ('﻿' + csv_content).encode('utf-8')
        resp = HttpResponse(csv_bytes, content_type='text/csv; charset=utf-8')
        resp['Content-Disposition'] = 'attachment; filename="testcases_template.csv"'
        return resp

    @action(detail=False, methods=['post'], url_path='import')
    def import_cases(self, request):
        """
        从 CSV 导入用例
        POST /api/testcases/import/
        Content-Type: multipart/form-data
        file: CSV 文件（可用 /template 接口下载模板）
        """
        upload = request.FILES.get('file')
        if not upload:
            return Response({'code': 40000, 'error': '请上传文件（file 字段）'}, status=status.HTTP_400_BAD_REQUEST)

        # 文件大小限制，避免超大文件拖垮内存
        if upload.size and upload.size > MAX_IMPORT_SIZE:
            return Response(
                {'code': 40000, 'error': f'文件过大，限制为 {MAX_IMPORT_SIZE // (1024 * 1024)}MB 以内'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 统一按 UTF-8 解析，兼容带 BOM
            content = upload.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            return Response({'code': 40000, 'error': '文件编码错误，请使用 UTF-8 保存'}, status=status.HTTP_400_BAD_REQUEST)

        f = io.StringIO(content)
        reader = csv.DictReader(f)

        created = 0
        updated = 0
        errors = []

        # 表头白名单校验，必须与模板一致（避免恶意隐藏列）
        raw_header = reader.fieldnames or []
        normalized_header = [h.strip() for h in raw_header]
        if normalized_header != CSV_HEADER:
            return Response(
                {
                    'code': 40000,
                    'error': '表头不符合模板，请先下载最新模板后再导入',
                    'detail': {
                        'expected': CSV_HEADER,
                        'got': normalized_header,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        def parse_bool(val):
            if val is None:
                return False
            v = str(val).strip().lower()
            return v in ('1', 'true', 'yes', 'y', '是')

        for idx, row in enumerate(reader, start=2):  # 从第 2 行开始（第 1 行是表头）
            if idx - 1 > MAX_IMPORT_ROWS:
                errors.append({'row': idx, 'errors': {'__all__': [f'超出最大导入行数限制：{MAX_IMPORT_ROWS} 行']}})
                break

            # 简单恶意内容检测：防止 CSV 注入 / XSS 等
            malicious = False
            suspicious_cells = {}
            for field in CSV_HEADER:
                cell_raw = row.get(field)
                cell = (cell_raw or '').strip()
                if not cell:
                    continue
                # 1) 公式注入：以 =,+,-,@ 开头
                if cell[0] in ('=', '+', '-', '@'):
                    malicious = True
                    suspicious_cells[field] = '疑似公式注入，请去掉以 =,+,-,@ 开头的内容'
                    continue
                # 2) 典型脚本 / URL 关键字
                lower = cell.lower()
                if any(x in lower for x in ('<script', '</script', 'javascript:', 'onerror=', 'onload=')):
                    malicious = True
                    suspicious_cells[field] = '疑似脚本代码，请移除 <script> / javascript: 等内容'

            if malicious:
                errors.append({'row': idx, 'errors': suspicious_cells})
                continue

            data = {
                'product': (row.get('product') or '').strip(),
                'module': (row.get('module') or '').strip(),
                'sub_module': (row.get('sub_module') or '').strip(),
                'test_point': (row.get('test_point') or '').strip(),
                'title': (row.get('title') or '').strip(),
                'description': (row.get('description') or '').strip(),
                'precondition': (row.get('precondition') or '').strip(),
                'steps': (row.get('steps') or '').strip(),
                'expected_result': (row.get('expected_result') or '').strip(),
                'actual_result': (row.get('actual_result') or '').strip(),
                'priority': (row.get('priority') or '').strip() or TestCase.Priority.MEDIUM,
                'status': TestCase.Status.DRAFT,
                'stage': (row.get('stage') or '').strip() or None,
                'case_type': (row.get('case_type') or '').strip(),
                'remark': (row.get('remark') or '').strip(),
            }

            # 判断是否已存在：按「产品 + 模块 + 子模块 + 用例名称」视为同一条用例
            existing = TestCase.objects.filter(
                product=data['product'],
                module=data['module'],
                sub_module=data['sub_module'],
                title=data['title'],
            ).first()

            user = getattr(request, 'user', None)

            if existing:
                # 已存在则更新
                serializer = TestCaseCreateUpdateSerializer(existing, data=data)
            else:
                serializer = TestCaseCreateUpdateSerializer(data=data)

            if serializer.is_valid():
                if existing:
                    # 批量导入更新：记录修改人
                    if user and user.is_authenticated:
                        serializer.save(updater=user)
                    else:
                        serializer.save()
                    updated += 1
                else:
                    # 批量导入新增：记录创建人 + 修改人
                    if user and user.is_authenticated:
                        serializer.save(creator=user, updater=user)
                    else:
                        serializer.save()
                    created += 1
            else:
                errors.append({'row': idx, 'errors': serializer.errors})

        result = {
            'code': 20000,
            'msg': 'Import finished',
            'data': {
                'created': created,
                'updated': updated,
                'failed': len(errors),
                'errors': errors[:50],  # 避免错误过多撑爆响应
            },
        }
        status_code = status.HTTP_200_OK if not errors else status.HTTP_207_MULTI_STATUS
        return Response(result, status=status_code)
