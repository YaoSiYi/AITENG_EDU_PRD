from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializers import (
    UserSerializer, UserRegisterSerializer, CustomTokenObtainPairSerializer,
    UserProfileUpdateSerializer, PasswordResetSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """用户视图集"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['register', 'login', 'guest_login']:
            return [AllowAny()]
        elif self.action in ['list', 'admin_list']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def list(self, request):
        """管理员用户列表（支持分页、搜索、筛选）"""
        queryset = User.objects.all().order_by('-created_at')

        # 搜索
        search = request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(nickname__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )

        # 角色筛选
        role = request.query_params.get('role', '')
        if role:
            queryset = queryset.filter(role=role)

        # 分页
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size

        total = queryset.count()
        users = queryset[start:end]

        return Response({
            'total': total,
            'page': page,
            'page_size': page_size,
            'results': UserSerializer(users, many=True).data
        })

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """用户注册"""
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': '注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def guest_login(self, request):
        """游客登录"""
        # 创建临时游客账号或返回游客token
        return Response({
            'message': '游客登录成功',
            'is_guest': True
        })

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """获取当前用户信息"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """修改密码"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # 验证参数
        if not old_password or not new_password:
            return Response(
                {'error': '原始密码和新密码不能为空'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证原始密码
        if not user.check_password(old_password):
            return Response(
                {'old_password': '原始密码不正确'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码长度
        if len(new_password) < 6 or len(new_password) > 20:
            return Response(
                {'new_password': '密码长度必须为 6-20 位字符'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证新密码不能与原密码相同
        if old_password == new_password:
            return Response(
                {'new_password': '新密码不能与原始密码相同'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 修改密码
        user.set_password(new_password)
        # 同时更新明文密码字段
        user.plain_password = new_password
        user.save()

        return Response({
            'message': '密码修改成功'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        """更新用户资料"""
        serializer = UserProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """重置密码"""
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO: 验证短信验证码
        phone = serializer.validated_data['phone']
        new_password = serializer.validated_data['new_password']

        try:
            user = User.objects.get(phone=phone)
            user.set_password(new_password)
            user.save()
            return Response({'message': '密码重置成功'})
        except User.DoesNotExist:
            return Response(
                {'error': '手机号不存在'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def wechat_login(self, request):
        """微信一键登录"""
        code = request.data.get('code')
        # TODO: 调用微信API获取openid
        # TODO: 查找或创建用户
        return Response({'message': '微信登录功能待实现'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def qq_login(self, request):
        """QQ一键登录"""
        code = request.data.get('code')
        # TODO: 调用QQ API获取openid
        # TODO: 查找或创建用户
        return Response({'message': 'QQ登录功能待实现'})


class CustomTokenObtainPairView(TokenObtainPairView):
    """自定义JWT登录视图"""
    serializer_class = CustomTokenObtainPairSerializer
