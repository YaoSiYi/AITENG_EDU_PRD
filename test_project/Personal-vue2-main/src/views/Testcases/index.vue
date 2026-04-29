<template>
  <div class="app-container">
    <!-- 搜索和操作栏 -->
    <div class="filter-container">
      <el-input
        v-model="listQuery.search"
        placeholder="搜索"
        style="width: 160px;"
        class="filter-item"
        clearable
        @keyup.enter.native="handleFilter"
      />
      <el-input
        v-model="listQuery.product"
        placeholder="产品（模糊）"
        clearable
        class="filter-item"
        style="width: 140px; margin-left: 10px;"
        @keyup.enter.native="handleFilter"
      />
      <el-input
        v-model="listQuery.module"
        placeholder="功能模块（模糊）"
        clearable
        class="filter-item"
        style="width: 140px; margin-left: 10px;"
        @keyup.enter.native="handleFilter"
      />
      <el-input
        v-model="listQuery.sub_module"
        placeholder="子模块（模糊）"
        clearable
        class="filter-item"
        style="width: 140px; margin-left: 10px;"
        @keyup.enter.native="handleFilter"
      />
      <el-input
        v-model="listQuery.test_point"
        placeholder="测试点（模糊）"
        clearable
        class="filter-item"
        style="width: 140px; margin-left: 10px;"
        @keyup.enter.native="handleFilter"
      />
      <el-select
        v-model="listQuery.priority"
        placeholder="优先级（精确）"
        clearable
        class="filter-item"
        style="width: 130px; margin-left: 10px;"
        @change="handleFilter"
      >
        <el-option label="严重" value="critical" />
        <el-option label="高" value="high" />
        <el-option label="中" value="medium" />
        <el-option label="低" value="low" />
      </el-select>
      <el-select
        v-model="listQuery.status"
        placeholder="状态（精确）"
        clearable
        class="filter-item"
        style="width: 120px; margin-left: 10px;"
        @change="handleFilter"
      >
        <el-option label="停用" value="draft" />
        <el-option label="启用" value="active" />
      </el-select>
      <el-select
        v-model="listQuery.is_smoke"
        placeholder="是否冒烟"
        clearable
        class="filter-item"
        style="width: 120px; margin-left: 10px;"
        @change="handleFilter"
      >
        <el-option label="是" :value="true" />
        <el-option label="否" :value="false" />
      </el-select>
      <el-input
        v-model="listQuery.case_type"
        placeholder="用例类型（模糊）"
        clearable
        class="filter-item"
        style="width: 150px; margin-left: 10px;"
        @keyup.enter.native="handleFilter"
      />
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter"
      >
        查询
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        icon="el-icon-refresh"
        @click="handleResetFilter"
      >
        重置
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-plus" @click="handleAdd">
        新建
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        icon="el-icon-download"
        @click="handleExport"
      >
        导出
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        icon="el-icon-upload2"
        @click="showImportDialog"
      >
        导入
      </el-button>
      <el-button
        class="filter-item"
        style="margin-left: 10px;"
        type="danger"
        icon="el-icon-delete"
        :disabled="multipleSelection.length === 0"
        @click="handleBatchDelete"
      >
        批量删除
      </el-button>
    </div>

    <!-- 数据表格 -->
    <div style="margin-top: 20px;">
      <el-table
        :key="tableKey"
        v-loading="listLoading"
        :data="list"
        border
        fit
        highlight-current-row
        style="width: 100%;"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="expand" width="40">
          <template slot-scope="{ row }">
            <div class="expand-wrapper">
              <div class="expand-item">
                <span class="expand-label">前置条件：</span>
                <span class="expand-value">{{ inlineText(row.precondition) }}</span>
              </div>
              <div class="expand-item">
                <span class="expand-label">步骤：</span>
                <span class="expand-value">{{ inlineText(row.steps) }}</span>
              </div>
              <div class="expand-item">
                <span class="expand-label">预期结果：</span>
                <span class="expand-value">{{ inlineText(row.expected_result) }}</span>
              </div>
              <div class="expand-item">
                <span class="expand-label">实际结果：</span>
                <span class="expand-value">{{ inlineText(row.actual_result) }}</span>
              </div>
              <div class="expand-item">
                <span class="expand-label">备注：</span>
                <span class="expand-value">{{ inlineText(row.remark) }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="ID" prop="id" align="center" width="180" show-overflow-tooltip />
        <el-table-column label="产品" min-width="120px">
          <template slot-scope="{ row }">
            <span>{{ row.product || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="模块" min-width="120px">
          <template slot-scope="{ row }">
            <span>{{ row.module || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="子模块" min-width="120px">
          <template slot-scope="{ row }">
            <span>{{ row.sub_module || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="测试点" min-width="160px" show-overflow-tooltip>
          <template slot-scope="{ row }">
            <span>{{ row.test_point || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="标题" min-width="160px">
          <template slot-scope="{ row }">
            <span class="link-type" @click="handleView(row)">{{ row.title || row.name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="描述" min-width="160px" show-overflow-tooltip>
          <template slot-scope="{ row }">
            <span>{{ row.description || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="优先级" width="100" align="center">
          <template slot-scope="{ row }">
            <el-tag :type="priorityTagType(row.priority)" size="small">
              {{ priorityLabel(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">
              {{ statusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="冒烟" width="90px" align="center">
          <template slot-scope="{ row }">
            <el-tag v-if="row.is_smoke" type="success" size="small">是</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="用例类型" width="100px" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.case_type || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="创建人" width="100px" align="center" show-overflow-tooltip>
          <template slot-scope="{ row }">
            <span>{{ row.creator_name || userDisplay(row.creator) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="修改人" width="100px" align="center" show-overflow-tooltip>
          <template slot-scope="{ row }">
            <span>{{ row.updater_name || userDisplay(row.updater) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="170px" align="center">
          <template slot-scope="{ row }">
            <span>{{ formatDateTime(row.created_at || row.createTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="更新时间" width="170px" align="center">
          <template slot-scope="{ row }">
            <span>{{ formatDateTime(row.updated_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="260" class-name="small-padding fixed-width">
          <template slot-scope="{ row }">
            <el-button type="text" size="mini" @click="handleView(row)">详情</el-button>
            <el-button type="text" size="mini" @click="handleEdit(row)">编辑</el-button>
            <el-button type="text" size="mini" class="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-show="total > 0" style="text-align: right; margin-top: 20px;">
      <pagination
        :total="total"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>

    <!-- 新建/编辑对话框 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible" width="520px" top="10vh">
      <el-form ref="dataForm" :model="temp" :rules="rules" label-width="90px">
        <el-form-item label="产品" prop="product">
          <el-input v-model="temp.product" placeholder="如：Web后台 / 移动端等" />
        </el-form-item>
        <el-form-item label="模块" prop="module">
          <el-input v-model="temp.module" placeholder="如：用户管理" />
        </el-form-item>
        <el-form-item label="子模块" prop="sub_module">
          <el-input v-model="temp.sub_module" placeholder="如：登录" />
        </el-form-item>
        <el-form-item label="测试点" prop="test_point">
          <el-input v-model="temp.test_point" placeholder="简要说明本用例关注的点" />
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="temp.title" placeholder="请输入用例标题（必填）" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="temp.description" type="textarea" :rows="2" placeholder="可填写简要背景说明" />
        </el-form-item>
        <el-form-item label="前置条件">
          <el-input v-model="temp.precondition" type="textarea" :rows="2" placeholder="执行前需要满足的条件" />
        </el-form-item>
        <el-form-item label="步骤">
          <el-input
            v-model="temp.steps"
            type="textarea"
            :rows="4"
            placeholder="1. 步骤一&#10;2. 步骤二"
          />
        </el-form-item>
        <el-form-item label="预期结果">
          <el-input v-model="temp.expected_result" type="textarea" :rows="3" placeholder="操作完成后的期望行为" />
        </el-form-item>
        <el-form-item label="实际结果">
          <el-input v-model="temp.actual_result" type="textarea" :rows="3" placeholder="执行后实际结果，可留空" />
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="temp.priority" placeholder="请选择" style="width: 100%;">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="temp.status" placeholder="请选择" style="width: 100%;">
            <el-option label="停用" value="draft" />
            <el-option label="启用" value="active" />
          </el-select>
        </el-form-item>
        <el-form-item label="冒烟用例">
          <el-switch v-model="temp.is_smoke" />
        </el-form-item>
        <el-form-item label="用例类型">
          <el-select v-model="temp.case_type" placeholder="请选择" style="width: 100%;">
            <el-option label="功能" value="功能" />
            <el-option label="回归" value="回归" />
            <el-option label="接口" value="接口" />
            <el-option label="性能" value="性能" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="temp.remark" type="textarea" :rows="2" placeholder="其他补充说明" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="dialogStatus === 'create' ? createData() : updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog title="用例详情" :visible.sync="detailVisible" width="560px">
      <div v-if="currentDetail" class="detail-form">
        <div class="detail-item"><span class="detail-label">ID：</span>{{ getCaseId(currentDetail) }}</div>
        <div class="detail-item"><span class="detail-label">创建人：</span>{{ currentDetail.creator_name || userDisplay(currentDetail.creator) }}</div>
        <div class="detail-item"><span class="detail-label">修改人：</span>{{ currentDetail.updater_name || userDisplay(currentDetail.updater) }}</div>
        <div class="detail-item"><span class="detail-label">创建时间：</span>{{ formatDateTime(currentDetail.created_at || currentDetail.createTime) }}</div>
        <div class="detail-item"><span class="detail-label">更新时间：</span>{{ formatDateTime(currentDetail.updated_at) }}</div>
        <div class="detail-item"><span class="detail-label">产品：</span>{{ currentDetail.product || '-' }}</div>
        <div class="detail-item"><span class="detail-label">模块：</span>{{ currentDetail.module || '-' }}</div>
        <div class="detail-item"><span class="detail-label">子模块：</span>{{ currentDetail.sub_module || '-' }}</div>
        <div class="detail-item"><span class="detail-label">测试点：</span>{{ currentDetail.test_point || '-' }}</div>
        <div class="detail-item"><span class="detail-label">标题：</span>{{ currentDetail.title || currentDetail.name || '-' }}</div>
        <div class="detail-item"><span class="detail-label">描述：</span>{{ currentDetail.description || '-' }}</div>
        <div class="detail-item"><span class="detail-label">前置条件：</span>{{ currentDetail.precondition || '-' }}</div>
        <div class="detail-item"><span class="detail-label">步骤：</span>{{ currentDetail.steps || '-' }}</div>
        <div class="detail-item"><span class="detail-label">预期结果：</span>{{ currentDetail.expected_result || '-' }}</div>
        <div class="detail-item"><span class="detail-label">实际结果：</span>{{ currentDetail.actual_result || '-' }}</div>
        <div class="detail-item">
          <span class="detail-label">优先级：</span>
          <el-tag :type="priorityTagType(currentDetail.priority)" size="small">
            {{ priorityLabel(currentDetail.priority) }}
          </el-tag>
        </div>
        <div class="detail-item"><span class="detail-label">状态：</span>{{ statusLabel(currentDetail.status) }}</div>
        <div class="detail-item"><span class="detail-label">是否冒烟：</span>{{ currentDetail.is_smoke ? '是' : '否' }}</div>
        <div class="detail-item"><span class="detail-label">用例类型：</span>{{ currentDetail.case_type || '-' }}</div>
        <div class="detail-item"><span class="detail-label">备注：</span>{{ currentDetail.remark || '-' }}</div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEditFromDetail">编辑</el-button>
      </div>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog title="导入用例" :visible.sync="importVisible" width="480px">
      <div class="import-tip">
        <p>1. 点击「下载模板」获取 CSV 模板并填写</p>
        <p>2. 上传填写完成的 CSV 文件</p>
      </div>
      <el-button
        type="primary"
        icon="el-icon-download"
        style="margin-bottom: 16px;"
        @click="handleDownloadTemplate"
      >
        下载模板
      </el-button>
      <el-upload
        ref="upload"
        :auto-upload="false"
        :limit="1"
        :on-change="handleFileChange"
        :on-exceed="handleFileExceed"
        accept=".csv"
        action="#"
      >
        <el-button slot="trigger" type="primary" plain>选择 CSV 文件</el-button>
      </el-upload>
      <p v-if="importFile" class="file-name">{{ importFile.name }}</p>
      <div slot="footer">
        <el-button @click="importVisible = false">取消</el-button>
        <el-button type="primary" :loading="importLoading" :disabled="!importFile" @click="handleImport">
          开始导入
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { parseTime } from '@/utils'
import {
  getTestcaseList,
  createTestcase,
  getTestcaseDetail,
  updateTestcase,
  partialUpdateTestcase,
  deleteTestcase,
  exportTestcases,
  downloadTestcaseTemplate,
  importTestcases
} from '@/api/testcases'

export default {
  name: 'Testcases',
  components: { Pagination },
  data() {
    return {
      tableKey: 0,
      list: [],
      total: 0,
      listLoading: false,
      submitLoading: false,
      listQuery: {
        page: 1,
        limit: 20,
        search: undefined,
        product: undefined,
        module: undefined,
        sub_module: undefined,
        test_point: undefined,
        priority: undefined,
        status: undefined,
        is_smoke: undefined,
        case_type: undefined
      },
      multipleSelection: [],
      temp: {
        id: undefined,
        product: '',
        module: '',
        sub_module: '',
        test_point: '',
        title: '',
        description: '',
        precondition: '',
        steps: '',
        expected_result: '',
        actual_result: '',
        priority: 'medium',
        status: 'active',
        is_smoke: false,
        case_type: '',
        remark: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: { update: '编辑用例', create: '新建用例' },
      rules: {
        title: [{ required: true, message: '标题为必填项', trigger: 'blur' }]
      },
      detailVisible: false,
      currentDetail: null,
      originalRow: null,
      importVisible: false,
      importFile: null,
      importLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    // 兼容后端返回 { results, count } 或 直接数组
    normalizeListResponse(res) {
      if (Array.isArray(res)) {
        return { list: res, total: res.length }
      }
      if (res && Array.isArray(res.results)) {
        return { list: res.results, total: res.count != null ? res.count : res.results.length }
      }
      return { list: [], total: 0 }
    },
    getList() {
      this.listLoading = true
      const params = {
        page: this.listQuery.page,
        limit: this.listQuery.limit
      }
      if (this.listQuery.search) params.search = this.listQuery.search
      if (this.listQuery.product) params.product = this.listQuery.product
      if (this.listQuery.module) params.module = this.listQuery.module
      if (this.listQuery.sub_module) params.sub_module = this.listQuery.sub_module
      if (this.listQuery.test_point) params.test_point = this.listQuery.test_point
      if (this.listQuery.priority) params.priority = this.listQuery.priority
      if (this.listQuery.status) params.status = this.listQuery.status
      if (this.listQuery.is_smoke !== undefined && this.listQuery.is_smoke !== null) {
        params.is_smoke = this.listQuery.is_smoke
      }
      if (this.listQuery.case_type) params.case_type = this.listQuery.case_type
      getTestcaseList(params)
        .then(res => {
          const { list, total } = this.normalizeListResponse(res)
          this.list = list
          this.total = total
        })
        .catch(() => {
          this.list = []
          this.total = 0
        })
        .finally(() => {
          this.listLoading = false
        })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleResetFilter() {
      this.listQuery = {
        page: 1,
        limit: this.listQuery.limit,
        search: undefined,
        product: undefined,
        module: undefined,
        sub_module: undefined,
        test_point: undefined,
        priority: undefined,
        status: undefined,
        is_smoke: undefined,
        case_type: undefined
      }
      this.getList()
    },
    handleAdd() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'] && this.$refs['dataForm'].clearValidate()
      })
    },
    handleView(row) {
      this.currentDetail = null
      this.detailVisible = true
      getTestcaseDetail(this.getCaseId(row))
        .then(data => {
          this.currentDetail = data
        })
        .catch(() => {
          this.$message.error('获取详情失败')
          this.currentDetail = { ...row }
        })
    },
    handleEdit(row) {
      const copy = Object.assign({}, row)
      copy.title = copy.title || copy.name
      this.temp = copy
      this.originalRow = Object.assign({}, row)
      this.originalRow.title = this.originalRow.title || this.originalRow.name
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'] && this.$refs['dataForm'].clearValidate()
      })
    },
    handleEditFromDetail() {
      this.detailVisible = false
      if (this.currentDetail) {
        this.handleEdit(this.currentDetail)
      }
    },
    handleDelete(row) {
      this.$confirm('确定删除该测试用例吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          return deleteTestcase(this.getCaseId(row))
        })
        .then(() => {
          this.$message.success('删除成功')
          this.getList()
        })
        .catch(err => {
          if (err !== 'cancel') this.$message.error(err && err.message ? err.message : '删除失败')
        })
    },
    handleBatchDelete() {
      if (this.multipleSelection.length === 0) {
        this.$message.warning('请至少选择一条数据')
        return
      }
      this.$confirm(`确定删除选中的 ${this.multipleSelection.length} 条用例吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          return Promise.all(this.multipleSelection.map(row => deleteTestcase(this.getCaseId(row))))
        })
        .then(() => {
          this.$message.success('批量删除成功')
          this.getList()
        })
        .catch(err => {
          if (err !== 'cancel') this.$message.error('批量删除失败')
        })
    },
    createData() {
      this.$refs['dataForm'].validate(valid => {
        if (!valid) return
        this.submitLoading = true
        createTestcase(this.temp)
          .then(() => {
            this.$message.success('创建成功')
            this.dialogFormVisible = false
            this.getList()
          })
          .catch(() => {
            this.$message.error('创建失败')
          })
          .finally(() => {
            this.submitLoading = false
          })
      })
    },
    updateData() {
      this.$refs['dataForm'].validate(valid => {
        if (!valid) return
        this.submitLoading = true
        const id = this.getCaseId(this.temp)
        const fields = ['product', 'module', 'sub_module', 'test_point', 'title', 'description', 'precondition', 'steps', 'expected_result', 'actual_result', 'priority', 'status', 'is_smoke', 'case_type', 'remark']
        const data = {}
        const orig = this.originalRow || {}
        fields.forEach(field => {
          const v1 = this.temp[field]
          const v2 = orig[field]
          if (v1 !== v2 && (v1 !== undefined || v2 !== undefined)) {
            data[field] = v1
          }
        })
        if (Object.keys(data).length === 0) {
          this.$message.info('没有修改')
          this.dialogFormVisible = false
          this.submitLoading = false
          return
        }
        partialUpdateTestcase(id, data)
          .then(() => {
            this.$message.success('更新成功')
            this.dialogFormVisible = false
            this.getList()
          })
          .catch(() => {
            this.$message.error('更新失败')
          })
          .finally(() => {
            this.submitLoading = false
          })
      })
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        product: '',
        module: '',
        sub_module: '',
        test_point: '',
        title: '',
        description: '',
        precondition: '',
        steps: '',
        expected_result: '',
        actual_result: '',
        priority: 'medium',
        status: 'active',
        is_smoke: false,
        case_type: '',
        remark: ''
      }
    },
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    getCaseId(row) {
      if (!row) return ''
      return row.public_id !== undefined && row.public_id !== null ? row.public_id : row.id
    },
    buildExportParams() {
      const p = {}
      if (this.listQuery.search) p.search = this.listQuery.search
      if (this.listQuery.product) p.product = this.listQuery.product
      if (this.listQuery.module) p.module = this.listQuery.module
      if (this.listQuery.sub_module) p.sub_module = this.listQuery.sub_module
      if (this.listQuery.test_point) p.test_point = this.listQuery.test_point
      if (this.listQuery.priority) p.priority = this.listQuery.priority
      if (this.listQuery.status) p.status = this.listQuery.status
      if (this.listQuery.is_smoke !== undefined && this.listQuery.is_smoke !== null) {
        p.is_smoke = this.listQuery.is_smoke
      }
      if (this.listQuery.case_type) p.case_type = this.listQuery.case_type
      return p
    },
    handleExport() {
      const params = this.multipleSelection.length > 0
        ? { ids: this.multipleSelection.map(r => this.getCaseId(r)).join(',') }
        : this.buildExportParams()

      if (this.multipleSelection.length > 1000) {
        this.$message.warning('一次最多导出 1000 条，当前已选 ' + this.multipleSelection.length + ' 条')
        return
      }

      exportTestcases(params)
        .then(blob => {
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `testcases_export_${parseTime(new Date(), '{y}{m}{d}{h}{i}{s}')}.csv`
          a.click()
          URL.revokeObjectURL(url)
          this.$message.success('导出成功')
        })
        .catch(() => {
          this.$message.error('导出失败')
        })
    },
    showImportDialog() {
      this.importVisible = true
      this.importFile = null
      this.$nextTick(() => {
        this.$refs.upload && this.$refs.upload.clearFiles()
      })
    },
    handleDownloadTemplate() {
      downloadTestcaseTemplate()
        .then(blob => {
          const url = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = 'testcases_template.csv'
          a.click()
          URL.revokeObjectURL(url)
          this.$message.success('模板已下载')
        })
        .catch(() => {
          this.$message.error('下载模板失败')
        })
    },
    handleFileChange(file) {
      this.importFile = file.raw
    },
    handleFileExceed() {
      this.$message.warning('只能上传 1 个文件')
    },
    handleImport() {
      if (!this.importFile) {
        this.$message.warning('请选择 CSV 文件')
        return
      }
      const formData = new FormData()
      formData.append('file', this.importFile)
      this.importLoading = true
      importTestcases(formData)
        .then(res => {
          const data = (res && res.data !== undefined) ? res.data : res
          const created = data.created ?? 0
          const failed = data.failed ?? 0
          const errors = data.errors || []
          let msg = `导入完成：成功 ${created} 条`
          if (failed > 0) {
            msg += `，失败 ${failed} 条`
            if (errors.length > 0) {
              const errStr = Array.isArray(errors) ? errors.slice(0, 3).join('；') : String(errors)
              msg += `。${errStr}${errors.length > 3 ? '...' : ''}`
            }
          }
          this.$message.success(msg)
          this.importVisible = false
          this.importFile = null
          this.$refs.upload && this.$refs.upload.clearFiles()
          this.getList()
        })
        .catch(e => {
          this.$message.error(e.message || '导入失败')
        })
        .finally(() => {
          this.importLoading = false
        })
    },
    formatDateTime(time) {
      if (!time) return '-'
      const date = new Date(time)
      if (isNaN(date.getTime())) {
        return '-'
      }
      return parseTime(date, '{y}-{m}-{d} {h}:{i}:{s}')
    },
    inlineText(text) {
      if (!text) return '—'
      return text.replace(/\n/g, '； ')
    },
    priorityTagType(priority) {
      const map = { critical: 'danger', high: 'danger', medium: 'warning', low: 'info' }
      return map[priority] || 'info'
    },
    priorityLabel(priority) {
      const map = { critical: '严重', high: '高', medium: '中', low: '低' }
      return map[priority] || '-'
    },
    statusTagType(status) {
      const map = { draft: 'info', active: 'success' }
      return map[status] || 'info'
    },
    statusLabel(status) {
      const map = { draft: '停用', active: '启用' }
      return map[status] || (status || '-')
    },
    userDisplay(val) {
      if (val == null || val === '') return '-'
      if (typeof val === 'object' && val !== null) {
        return val.name || val.username || val.nickname || '-'
      }
      return '-'
    }
  }
}
</script>

<style scoped>
.link-type {
  color: #409eff;
  cursor: pointer;
}
.link-type:hover {
  text-decoration: underline;
}
.danger {
  color: #f56c6c;
}
.detail-form .detail-item {
  margin-bottom: 12px;
  line-height: 1.6;
}
.detail-form .detail-label {
  display: inline-block;
  width: 90px;
  color: #909399;
}
.expand-wrapper {
  padding: 8px 16px;
  font-size: 13px;
  line-height: 1.6;
}
.expand-item {
  margin-bottom: 6px;
}
.expand-label {
  display: inline-block;
  width: 80px;
  color: #909399;
}
.expand-value {
  white-space: normal;
  word-break: break-all;
}
.import-tip {
  margin-bottom: 16px;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}
.import-tip p {
  margin: 4px 0;
}
.file-name {
  margin-top: 8px;
  font-size: 13px;
  color: #909399;
}
</style>
