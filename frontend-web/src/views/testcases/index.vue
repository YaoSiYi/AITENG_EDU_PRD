<template>
  <div class="testcases-container">
    <!-- 页面标题和导航 -->
    <div class="page-header">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>测试用例管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 搜索和操作栏 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="queryParams" class="filter-form">
        <el-form-item label="关键字">
          <el-input
            v-model="queryParams.keyword"
            placeholder="搜索标题/描述/测试点"
            clearable
            style="width: 200px"
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item label="产品">
          <el-input
            v-model="queryParams.product"
            placeholder="产品名称"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="模块">
          <el-input
            v-model="queryParams.module"
            placeholder="功能模块"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="queryParams.severity" placeholder="请选择" clearable style="width: 120px">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="queryParams.priority" placeholder="请选择" clearable style="width: 120px">
            <el-option label="紧急" value="critical" />
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryParams.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="草稿" value="draft" />
            <el-option label="有效" value="active" />
            <el-option label="已废弃" value="deprecated" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="指派人员">
          <el-select v-model="queryParams.assignee" placeholder="请选择" clearable style="width: 120px">
            <el-option
              v-for="user in assignableUsers"
              :key="user.id"
              :label="user.nickname"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="queryParams.my_assigned">只看我的指派</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleQuery">查询</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <div class="action-buttons">
        <el-button type="primary" icon="Plus" @click="handleAdd">新建</el-button>
        <el-button icon="Download" @click="handleExport">导出</el-button>
        <el-button icon="Upload" @click="showImportDialog">导入</el-button>
        <el-button
          type="danger"
          icon="Delete"
          :disabled="selectedRows.length === 0"
          @click="handleBatchDelete"
        >
          批量删除
        </el-button>
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="tableData"
        border
        stripe
        :row-class-name="getRowClassName"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column type="expand">
          <template #default="{ row }">
            <div class="expand-content">
              <p><strong>前置条件：</strong>{{ row.precondition || '-' }}</p>
              <p><strong>测试步骤：</strong>{{ row.steps || '-' }}</p>
              <p><strong>预期结果：</strong>{{ row.expected_result || '-' }}</p>
              <p><strong>实际结果：</strong>{{ row.actual_result || '-' }}</p>
              <p><strong>备注：</strong>{{ row.remark || '-' }}</p>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="id" label="ID" width="180" show-overflow-tooltip />
        <el-table-column prop="product" label="产品" width="120" />
        <el-table-column prop="module" label="模块" width="120" />
        <el-table-column prop="sub_module" label="子模块" width="120" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link type="primary" @click="handleView(row)">{{ row.title }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="severity" label="严重程度" width="110" align="center">
          <template #default="{ row }">
            <el-dropdown
              @command="(val) => handleQuickUpdate(row, 'severity', val)"
              :disabled="isRowDisabled(row)"
            >
              <el-tag :type="getSeverityType(row.severity)" size="small" :style="{ cursor: isRowDisabled(row) ? 'not-allowed' : 'pointer' }">
                <el-icon style="vertical-align: middle; margin-right: 4px">
                  <component :is="getSeverityIcon(row.severity)" />
                </el-icon>
                {{ getSeverityLabel(row.severity) }}
                <el-icon class="el-icon--right" v-if="!isRowDisabled(row)"><ArrowDown /></el-icon>
              </el-tag>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="high">高</el-dropdown-item>
                  <el-dropdown-item command="medium">中</el-dropdown-item>
                  <el-dropdown-item command="low">低</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="priority" label="优先级" width="100" align="center">
          <template #default="{ row }">
            <el-dropdown
              @command="(val) => handleQuickUpdate(row, 'priority', val)"
              :disabled="isRowDisabled(row)"
            >
              <el-tag :type="getPriorityType(row.priority)" size="small" :style="{ cursor: isRowDisabled(row) ? 'not-allowed' : 'pointer' }">
                {{ getPriorityLabel(row.priority) }}
                <el-icon class="el-icon--right" v-if="!isRowDisabled(row)"><ArrowDown /></el-icon>
              </el-tag>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="critical">紧急</el-dropdown-item>
                  <el-dropdown-item command="high">高</el-dropdown-item>
                  <el-dropdown-item command="medium">中</el-dropdown-item>
                  <el-dropdown-item command="low">低</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template #default="{ row }">
            <el-dropdown @command="(val) => handleQuickUpdate(row, 'status', val)">
              <el-tag :type="getStatusType(row.status)" size="small" style="cursor: pointer">
                {{ getStatusLabel(row.status) }}
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-tag>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="draft">草稿</el-dropdown-item>
                  <el-dropdown-item command="active">有效</el-dropdown-item>
                  <el-dropdown-item command="deprecated">已废弃</el-dropdown-item>
                  <el-dropdown-item command="closed">已关闭</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="stage" label="阶段" width="110" align="center">
          <template #default="{ row }">
            <el-dropdown
              @command="(val) => handleQuickUpdate(row, 'stage', val)"
              :disabled="isRowDisabled(row)"
            >
              <el-tag :type="getStageType(row.stage)" size="small" :style="{ cursor: isRowDisabled(row) ? 'not-allowed' : 'pointer' }">
                {{ getStageLabel(row.stage) }}
                <el-icon class="el-icon--right" v-if="!isRowDisabled(row)"><ArrowDown /></el-icon>
              </el-tag>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="null">未设置</el-dropdown-item>
                  <el-dropdown-item command="smoke">冒烟测试</el-dropdown-item>
                  <el-dropdown-item command="pre_prod">预发环境</el-dropdown-item>
                  <el-dropdown-item command="production">生产环境</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="reproduce_steps" label="复现步骤" width="120" align="center">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              size="small"
              :disabled="isRowDisabled(row)"
              @click="handleEditReproduceSteps(row)"
            >
              <span v-if="row.reproduce_steps && row.reproduce_steps.length > 0">
                编辑({{ row.reproduce_steps.length }})
              </span>
              <span v-else>添加</span>
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="assignee_name" label="指派人员" width="100" align="center">
          <template #default="{ row }">
            <el-dropdown @command="(val) => handleAssign(row, val)" :disabled="isRowDisabled(row)">
              <el-tag :type="row.assignee_name ? 'success' : 'info'" size="small" :style="{ cursor: isRowDisabled(row) ? 'not-allowed' : 'pointer' }">
                {{ row.assignee_name || '未指派' }}
                <el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-tag>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item :command="null">取消指派</el-dropdown-item>
                  <el-dropdown-item
                    v-for="user in assignableUsers"
                    :key="user.id"
                    :command="user.id"
                  >
                    {{ user.nickname }}
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
        <el-table-column prop="creator_name" label="创建人" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right" align="center">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">详情</el-button>
            <el-button
              type="primary"
              link
              size="small"
              :disabled="isRowDisabled(row)"
              @click="handleEdit(row)"
            >编辑</el-button>
            <el-button
              type="danger"
              link
              size="small"
              :disabled="isRowDisabled(row)"
              @click="handleDelete(row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="queryParams.page"
        v-model:page-size="queryParams.limit"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleQuery"
        @current-change="handleQuery"
      />
    </el-card>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <!-- 复用用例按钮 - 仅在新建模式显示 -->
      <div v-if="dialogMode === 'add'" style="margin-bottom: 16px; padding: 12px; background: #f0f9ff; border-radius: 4px; border: 1px solid #91d5ff">
        <el-button type="success" icon="CopyDocument" size="small" @click="showReuseDialog">
          复用用例
        </el-button>
        <span style="margin-left: 10px; color: #1890ff; font-size: 13px">
          💡 可通过输入用例ID快速复制已有用例信息
        </span>
      </div>

      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
        <el-form-item label="产品" prop="product">
          <el-input v-model="formData.product" placeholder="如：教务管理系统" />
        </el-form-item>
        <el-form-item label="模块" prop="module">
          <el-input v-model="formData.module" placeholder="如：题库管理" />
        </el-form-item>
        <el-form-item label="子模块" prop="sub_module">
          <el-input v-model="formData.sub_module" placeholder="如：题目列表" />
        </el-form-item>
        <el-form-item label="测试点" prop="test_point">
          <el-input v-model="formData.test_point" placeholder="简要说明测试关注点" />
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入用例标题（必填）" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="formData.description" type="textarea" :rows="2" placeholder="简要背景说明" />
        </el-form-item>
        <el-form-item label="前置条件">
          <el-input v-model="formData.precondition" type="textarea" :rows="2" placeholder="执行前需满足的条件" />
        </el-form-item>
        <el-form-item label="测试步骤">
          <el-input v-model="formData.steps" type="textarea" :rows="4" placeholder="1. 步骤一&#10;2. 步骤二" />
        </el-form-item>
        <el-form-item label="预期结果">
          <el-input v-model="formData.expected_result" type="textarea" :rows="3" placeholder="操作完成后的期望行为" />
        </el-form-item>
        <el-form-item label="实际结果">
          <el-input v-model="formData.actual_result" type="textarea" :rows="3" placeholder="执行后实际结果" />
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="formData.severity" placeholder="请选择" style="width: 100%">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="formData.priority" placeholder="请选择" style="width: 100%">
            <el-option label="紧急" value="critical" />
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="有效" value="active" />
            <el-option label="已废弃" value="deprecated" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="阶段">
          <el-select v-model="formData.stage" placeholder="请选择" clearable style="width: 100%">
            <el-option label="冒烟测试" value="smoke" />
            <el-option label="预发环境" value="pre_prod" />
            <el-option label="生产环境" value="production" />
          </el-select>
        </el-form-item>
        <el-form-item label="指派人员">
          <el-select v-model="formData.assignee" placeholder="请选择指派人员" clearable style="width: 100%">
            <el-option
              v-for="user in assignableUsers"
              :key="user.id"
              :label="user.nickname"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="复现步骤">
          <div class="reproduce-steps-editor">
            <el-button type="primary" size="small" @click="addReproduceStep('text')">添加文字</el-button>
            <el-button type="success" size="small" @click="addReproduceStep('image')">添加图片</el-button>
            <div v-if="formData.reproduce_steps && formData.reproduce_steps.length > 0" class="steps-list">
              <div
                v-for="(step, index) in formData.reproduce_steps"
                :key="index"
                class="step-item"
              >
                <div class="step-header">
                  <span class="step-number">步骤 {{ index + 1 }}</span>
                  <div class="step-actions">
                    <el-button type="primary" link size="small" @click="moveStepUp(index)" :disabled="index === 0">上移</el-button>
                    <el-button type="primary" link size="small" @click="moveStepDown(index)" :disabled="index === formData.reproduce_steps.length - 1">下移</el-button>
                    <el-button type="danger" link size="small" @click="removeReproduceStep(index)">删除</el-button>
                  </div>
                </div>
                <el-input
                  v-if="step.type === 'text'"
                  v-model="step.content"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入步骤描述"
                />
                <div v-else-if="step.type === 'image'" class="image-upload-area">
                  <el-upload
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="(file) => handleImageChange(file, index)"
                    accept="image/jpeg,image/jpg,image/png,image/gif,image/webp,image/bmp"
                    drag
                  >
                    <div v-if="!step.content" class="upload-placeholder">
                      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                      <div class="el-upload__text">拖拽图片到此处或<em>点击上传</em></div>
                      <div class="el-upload__tip">支持 JPG/PNG/GIF/WEBP/BMP，最大分辨率 2048x1280</div>
                    </div>
                    <img v-else :src="step.content" class="uploaded-image" alt="步骤图片" />
                  </el-upload>
                </div>
              </div>
            </div>
            <div v-else class="empty-steps">
              <el-empty description="暂无复现步骤" :image-size="80" />
            </div>
          </div>
        </el-form-item>
        <el-form-item label="用例类型">
          <el-input v-model="formData.case_type" placeholder="如：功能、接口、性能" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="formData.remark" type="textarea" :rows="2" placeholder="其他补充说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 复用用例对话框 -->
    <el-dialog
      v-model="reuseDialogVisible"
      title="复用用例"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form label-width="100px">
        <el-form-item label="用例ID">
          <el-input
            v-model="reuseTestcaseId"
            placeholder="请输入要复用的用例ID"
            clearable
            @keyup.enter="handleReuse"
          >
            <template #append>
              <el-button type="primary" @click="handleReuse" :loading="reuseLoading">
                复用
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-alert
          title="使用说明"
          type="info"
          :closable="false"
          style="margin-top: 10px"
        >
          <div style="font-size: 13px; line-height: 1.8; color: #606266">
            <p style="margin: 0 0 8px 0">📋 <strong>如何使用：</strong></p>
            <p style="margin: 0 0 4px 0; padding-left: 20px">1. 在列表的"ID"列中复制用例ID</p>
            <p style="margin: 0 0 4px 0; padding-left: 20px">2. 粘贴到上方输入框中</p>
            <p style="margin: 0 0 4px 0; padding-left: 20px">3. 点击"复用"按钮</p>
            <p style="margin: 8px 0 0 0">✨ <strong>复用后：</strong></p>
            <p style="margin: 0 0 4px 0; padding-left: 20px">• 自动填充所有用例信息到表单</p>
            <p style="margin: 0 0 4px 0; padding-left: 20px">• 标题自动添加"(复制)"后缀</p>
            <p style="margin: 0; padding-left: 20px">• 状态默认设为"草稿"</p>
          </div>
        </el-alert>
      </el-form>
      <template #footer>
        <el-button @click="reuseDialogVisible = false">取消</el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="测试用例详情" width="600px">
      <el-descriptions v-if="currentDetail" :column="1" border>
        <el-descriptions-item label="ID">{{ currentDetail.id }}</el-descriptions-item>
        <el-descriptions-item label="产品">{{ currentDetail.product || '-' }}</el-descriptions-item>
        <el-descriptions-item label="模块">{{ currentDetail.module || '-' }}</el-descriptions-item>
        <el-descriptions-item label="子模块">{{ currentDetail.sub_module || '-' }}</el-descriptions-item>
        <el-descriptions-item label="测试点">{{ currentDetail.test_point || '-' }}</el-descriptions-item>
        <el-descriptions-item label="标题">{{ currentDetail.title }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ currentDetail.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="前置条件">{{ currentDetail.precondition || '-' }}</el-descriptions-item>
        <el-descriptions-item label="测试步骤">
          <pre style="white-space: pre-wrap">{{ currentDetail.steps || '-' }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="预期结果">{{ currentDetail.expected_result || '-' }}</el-descriptions-item>
        <el-descriptions-item label="实际结果">{{ currentDetail.actual_result || '-' }}</el-descriptions-item>
        <el-descriptions-item label="严重程度">
          <el-tag :type="getSeverityType(currentDetail.severity)">
            <el-icon style="vertical-align: middle; margin-right: 4px">
              <component :is="getSeverityIcon(currentDetail.severity)" />
            </el-icon>
            {{ getSeverityLabel(currentDetail.severity) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityType(currentDetail.priority)">
            {{ getPriorityLabel(currentDetail.priority) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentDetail.status)">
            {{ getStatusLabel(currentDetail.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="阶段">
          <el-tag :type="getStageType(currentDetail.stage)" size="small">
            {{ getStageLabel(currentDetail.stage) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="指派人员">{{ currentDetail.assignee_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="复现步骤">
          <el-button
            v-if="currentDetail.reproduce_steps && currentDetail.reproduce_steps.length > 0"
            type="primary"
            link
            size="small"
            @click="handleViewReproduceSteps(currentDetail)"
          >
            查看({{ currentDetail.reproduce_steps.length }}步)
          </el-button>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="用例类型">{{ currentDetail.case_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注">{{ currentDetail.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ currentDetail.creator_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="修改人">{{ currentDetail.updater_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(currentDetail.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDateTime(currentDetail.updated_at) }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleEditFromDetail">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 导入对话框 -->
    <el-dialog v-model="importVisible" title="导入测试用例" width="500px">
      <div class="import-tips">
        <p>1. 点击「下载模板」获取CSV模板并填写</p>
        <p>2. 上传填写完成的CSV文件</p>
      </div>
      <el-button type="primary" icon="Download" style="margin-bottom: 16px" @click="handleDownloadTemplate">
        下载模板
      </el-button>
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :limit="1"
        :on-change="handleFileChange"
        accept=".csv"
        drag
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <template #tip>
          <div class="el-upload__tip">只能上传CSV文件，且不超过2MB</div>
        </template>
      </el-upload>
      <template #footer>
        <el-button @click="importVisible = false">取消</el-button>
        <el-button type="primary" :loading="importLoading" :disabled="!importFile" @click="handleImport">
          开始导入
        </el-button>
      </template>
    </el-dialog>
    <!-- 复现步骤查看对话框 -->
    <el-dialog v-model="reproduceStepsVisible" title="复现步骤" width="700px">
      <div v-if="currentReproduceSteps.length > 0" class="reproduce-steps-viewer">
        <div
          v-for="(step, index) in currentReproduceSteps"
          :key="index"
          class="step-viewer-item"
        >
          <div class="step-viewer-header">步骤 {{ index + 1 }}</div>
          <div v-if="step.type === 'text'" class="step-text-content">
            {{ step.content }}
          </div>
          <div v-else-if="step.type === 'image'" class="step-image-content">
            <img
              :src="step.content"
              class="step-thumbnail"
              @mouseenter="enlargedImage = step.content"
              @mouseleave="enlargedImage = null"
              @click="enlargedImage = null"
              alt="步骤图片"
            />
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无复现步骤" />
      <template #footer>
        <el-button @click="reproduceStepsVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 复现步骤编辑对话框 -->
    <el-dialog v-model="reproduceStepsEditVisible" title="编辑复现步骤" width="700px">
      <div class="reproduce-steps-editor">
        <div style="margin-bottom: 16px">
          <el-button type="primary" size="small" @click="addEditingStep('text')">添加文字</el-button>
          <el-button type="success" size="small" @click="addEditingStep('image')">添加图片</el-button>
        </div>
        <div v-if="editingReproduceSteps.length > 0" class="steps-list">
          <div
            v-for="(step, index) in editingReproduceSteps"
            :key="index"
            class="step-item"
          >
            <div class="step-header">
              <span class="step-number">步骤 {{ index + 1 }}</span>
              <div class="step-actions">
                <el-button type="primary" link size="small" @click="moveEditingStepUp(index)" :disabled="index === 0">上移</el-button>
                <el-button type="primary" link size="small" @click="moveEditingStepDown(index)" :disabled="index === editingReproduceSteps.length - 1">下移</el-button>
                <el-button type="danger" link size="small" @click="removeEditingStep(index)">删除</el-button>
              </div>
            </div>
            <el-input
              v-if="step.type === 'text'"
              v-model="step.content"
              type="textarea"
              :rows="2"
              placeholder="请输入步骤描述"
            />
            <div v-else-if="step.type === 'image'" class="image-upload-area">
              <el-upload
                :auto-upload="false"
                :show-file-list="false"
                :on-change="(file) => handleEditingImageChange(file, index)"
                accept="image/jpeg,image/jpg,image/png,image/gif,image/webp,image/bmp"
                drag
              >
                <div v-if="!step.content" class="upload-placeholder">
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">拖拽图片到此处或<em>点击上传</em></div>
                  <div class="el-upload__tip">支持 JPG/PNG/GIF/WEBP/BMP，最大分辨率 2048x1280</div>
                </div>
                <img v-else :src="step.content" class="uploaded-image" alt="步骤图片" />
              </el-upload>
            </div>
          </div>
        </div>
        <div v-else class="empty-steps">
          <el-empty description="暂无复现步骤" :image-size="80" />
        </div>
      </div>
      <template #footer>
        <el-button @click="reproduceStepsEditVisible = false">取消</el-button>
        <el-button type="primary" @click="saveReproduceSteps">保存</el-button>
      </template>
    </el-dialog>

    <!-- 图片放大查看 -->
    <div v-if="enlargedImage" class="image-overlay" @click="enlargedImage = null">
      <img :src="enlargedImage" class="enlarged-image" alt="放大图片" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled, ArrowDown, Warning, InfoFilled, CircleCheck, CopyDocument } from '@element-plus/icons-vue'
import { formatDateTime } from '@/utils/datetime'
import {
  getTestcaseList,
  createTestcase,
  getTestcaseDetail,
  updateTestcase,
  partialUpdateTestcase,
  deleteTestcase,
  exportTestcases,
  downloadTestcaseTemplate,
  importTestcases,
  getAssignableUsers
} from '@/api/testcases'

// 数据
const loading = ref(false)
const tableData = ref([])
const total = ref(0)
const selectedRows = ref([])

const queryParams = reactive({
  page: 1,
  limit: 20,
  keyword: '',
  product: '',
  module: '',
  severity: '',
  priority: '',
  status: '',
  assignee: '',
  my_assigned: false
})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const dialogMode = ref('add')
const submitLoading = ref(false)
const formRef = ref(null)

const formData = reactive({
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
  severity: 'medium',
  priority: 'medium',
  status: 'active',
  stage: null,
  reproduce_steps: [],
  assignee: null,
  case_type: '',
  remark: ''
})

const formRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }]
}

// 详情对话框
const detailVisible = ref(false)
const currentDetail = ref(null)

// 复现步骤查看对话框
const reproduceStepsVisible = ref(false)
const currentReproduceSteps = ref([])
const enlargedImage = ref(null)

// 复现步骤编辑对话框
const reproduceStepsEditVisible = ref(false)
const currentEditingRow = ref(null)
const editingReproduceSteps = ref([])

// 导入对话框
const importVisible = ref(false)
const importLoading = ref(false)
const importFile = ref(null)
const uploadRef = ref(null)

// 可指派用户列表
const assignableUsers = ref([])

// 复用用例对话框
const reuseDialogVisible = ref(false)
const reuseTestcaseId = ref('')
const reuseLoading = ref(false)

// 方法
const fetchList = async () => {
  loading.value = true
  try {
    const params = { ...queryParams }
    // 移除空值参数
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null) {
        delete params[key]
      }
    })

    const res = await getTestcaseList(params)
    tableData.value = res.results || []
    total.value = res.count || 0
  } catch (error) {
    ElMessage.error('获取列表失败')
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryParams.page = 1
  fetchList()
}

const handleReset = () => {
  Object.assign(queryParams, {
    page: 1,
    limit: 20,
    keyword: '',
    product: '',
    module: '',
    severity: '',
    priority: '',
    status: '',
    assignee: '',
    my_assigned: false
  })
  fetchList()
}

const handleAdd = () => {
  dialogMode.value = 'add'
  dialogTitle.value = '新建测试用例'
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogMode.value = 'edit'
  dialogTitle.value = '编辑测试用例'
  Object.assign(formData, row)
  dialogVisible.value = true
}

const handleView = async (row) => {
  try {
    const res = await getTestcaseDetail(row.id)
    currentDetail.value = res
    detailVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

const handleEditFromDetail = () => {
  detailVisible.value = false
  handleEdit(currentDetail.value)
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定删除该测试用例吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteTestcase(row.id)
      ElMessage.success('删除成功')
      fetchList()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleBatchDelete = () => {
  ElMessageBox.confirm(`确定删除选中的 ${selectedRows.value.length} 条用例吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await Promise.all(selectedRows.value.map(row => deleteTestcase(row.id)))
      ElMessage.success('批量删除成功')
      fetchList()
    } catch (error) {
      ElMessage.error('批量删除失败')
    }
  })
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (dialogMode.value === 'add') {
        await createTestcase(formData)
        ElMessage.success('创建成功')
      } else {
        await partialUpdateTestcase(formData.id, formData)
        ElMessage.success('更新成功')
      }
      dialogVisible.value = false
      fetchList()
    } catch (error) {
      ElMessage.error(dialogMode.value === 'add' ? '创建失败' : '更新失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDialogClose = () => {
  formRef.value?.resetFields()
  resetForm()
}

const resetForm = () => {
  Object.assign(formData, {
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
    severity: 'medium',
    priority: 'medium',
    status: 'active',
    stage: null,
    reproduce_steps: [],
    assignee: null,
    case_type: '',
    remark: ''
  })
}

const handleSelectionChange = (selection) => {
  selectedRows.value = selection
}

const handleExport = async () => {
  try {
    const params = selectedRows.value.length > 0
      ? { ids: selectedRows.value.map(r => r.id).join(',') }
      : { ...queryParams }

    const blob = await exportTestcases(params)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `testcases_${Date.now()}.csv`
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const showImportDialog = () => {
  importVisible.value = true
  importFile.value = null
  uploadRef.value?.clearFiles()
}

const handleDownloadTemplate = async () => {
  try {
    const blob = await downloadTestcaseTemplate()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'testcases_template.csv'
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success('模板已下载')
  } catch (error) {
    ElMessage.error('下载模板失败')
  }
}

const handleFileChange = (file) => {
  importFile.value = file.raw
}

const handleImport = async () => {
  if (!importFile.value) {
    ElMessage.warning('请选择CSV文件')
    return
  }

  const formData = new FormData()
  formData.append('file', importFile.value)

  importLoading.value = true
  try {
    const res = await importTestcases(formData)
    const data = res.data || res
    const created = data.created || 0
    const updated = data.updated || 0
    const failed = data.failed || 0

    ElMessage.success(`导入完成：新增 ${created} 条，更新 ${updated} 条，失败 ${failed} 条`)
    importVisible.value = false
    fetchList()
  } catch (error) {
    ElMessage.error('导入失败')
  } finally {
    importLoading.value = false
  }
}

// 快速更新字段
const handleQuickUpdate = async (row, field, value) => {
  try {
    const updateData = { [field]: value }
    await partialUpdateTestcase(row.id, updateData)

    // 更新本地数据
    row[field] = value

    const fieldLabels = {
      severity: '严重程度',
      priority: '优先级',
      status: '状态',
      stage: '阶段',
      assignee: '指派人员'
    }
    ElMessage.success(`${fieldLabels[field]}已更新`)
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 辅助方法
const getSeverityType = (severity) => {
  const map = { high: 'danger', medium: 'warning', low: 'success' }
  return map[severity] || 'info'
}

const getSeverityLabel = (severity) => {
  const map = { high: '高', medium: '中', low: '低' }
  return map[severity] || '-'
}

const getSeverityIcon = (severity) => {
  const map = { high: 'Warning', medium: 'InfoFilled', low: 'CircleCheck' }
  return map[severity] || 'InfoFilled'
}

const getPriorityType = (priority) => {
  const map = { critical: 'danger', high: 'danger', medium: 'warning', low: 'info' }
  return map[priority] || 'info'
}

const getPriorityLabel = (priority) => {
  const map = { critical: '紧急', high: '高', medium: '中', low: '低' }
  return map[priority] || '-'
}

const getStatusType = (status) => {
  const map = { draft: 'info', active: 'success', deprecated: 'warning', closed: 'primary' }
  return map[status] || 'info'
}

const getStatusLabel = (status) => {
  const map = { draft: '草稿', active: '有效', deprecated: '已废弃', closed: '已关闭' }
  return map[status] || '-'
}

const getStageType = (stage) => {
  const map = { smoke: 'warning', pre_prod: 'primary', production: 'danger' }
  return map[stage] || 'info'
}

const getStageLabel = (stage) => {
  const map = { smoke: '冒烟测试', pre_prod: '预发环境', production: '生产环境' }
  return map[stage] || '未设置'
}

// 判断行是否禁用编辑
const isRowDisabled = (row) => {
  return row.status === 'closed' || row.status === 'deprecated'
}

// 获取行的 class name
const getRowClassName = ({ row }) => {
  if (row.status === 'closed') {
    return 'row-closed'
  }
  if (row.status === 'deprecated') {
    return 'row-deprecated'
  }
  return ''
}

// 复现步骤相关函数
const addReproduceStep = (type) => {
  if (!formData.reproduce_steps) {
    formData.reproduce_steps = []
  }
  formData.reproduce_steps.push({
    type: type,
    content: ''
  })
}

const removeReproduceStep = (index) => {
  formData.reproduce_steps.splice(index, 1)
}

const moveStepUp = (index) => {
  if (index > 0) {
    const temp = formData.reproduce_steps[index]
    formData.reproduce_steps[index] = formData.reproduce_steps[index - 1]
    formData.reproduce_steps[index - 1] = temp
  }
}

const moveStepDown = (index) => {
  if (index < formData.reproduce_steps.length - 1) {
    const temp = formData.reproduce_steps[index]
    formData.reproduce_steps[index] = formData.reproduce_steps[index + 1]
    formData.reproduce_steps[index + 1] = temp
  }
}

const handleImageChange = (file, index) => {
  const reader = new FileReader()
  const img = new Image()

  reader.onload = (e) => {
    img.src = e.target.result

    img.onload = () => {
      // 检查分辨率
      if (img.width > 2048 || img.height > 1280) {
        ElMessage.warning(`图片分辨率过大（${img.width}x${img.height}），最大支持 2048x1280`)
        return
      }

      // 保存 base64 图片
      formData.reproduce_steps[index].content = e.target.result
    }
  }

  reader.readAsDataURL(file.raw)
}

const handleViewReproduceSteps = (row) => {
  currentReproduceSteps.value = row.reproduce_steps || []
  reproduceStepsVisible.value = true
}

const handleEditReproduceSteps = (row) => {
  currentEditingRow.value = row
  editingReproduceSteps.value = JSON.parse(JSON.stringify(row.reproduce_steps || []))
  reproduceStepsEditVisible.value = true
}

const addEditingStep = (type) => {
  editingReproduceSteps.value.push({
    type: type,
    content: ''
  })
}

const removeEditingStep = (index) => {
  editingReproduceSteps.value.splice(index, 1)
}

const moveEditingStepUp = (index) => {
  if (index > 0) {
    const temp = editingReproduceSteps.value[index]
    editingReproduceSteps.value[index] = editingReproduceSteps.value[index - 1]
    editingReproduceSteps.value[index - 1] = temp
  }
}

const moveEditingStepDown = (index) => {
  if (index < editingReproduceSteps.value.length - 1) {
    const temp = editingReproduceSteps.value[index]
    editingReproduceSteps.value[index] = editingReproduceSteps.value[index + 1]
    editingReproduceSteps.value[index + 1] = temp
  }
}

const handleEditingImageChange = (file, index) => {
  const reader = new FileReader()
  const img = new Image()

  reader.onload = (e) => {
    img.src = e.target.result

    img.onload = () => {
      // 检查分辨率
      if (img.width > 2048 || img.height > 1280) {
        ElMessage.warning(`图片分辨率过大（${img.width}x${img.height}），最大支持 2048x1280`)
        return
      }

      // 保存 base64 图片
      editingReproduceSteps.value[index].content = e.target.result
    }
  }

  reader.readAsDataURL(file.raw)
}

const saveReproduceSteps = async () => {
  if (!currentEditingRow.value) return

  try {
    await partialUpdateTestcase(currentEditingRow.value.id, {
      reproduce_steps: editingReproduceSteps.value
    })

    // 更新本地数据
    currentEditingRow.value.reproduce_steps = editingReproduceSteps.value

    reproduceStepsEditVisible.value = false
    ElMessage.success('复现步骤已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 指派人员
const handleAssign = async (row, assigneeId) => {
  try {
    await partialUpdateTestcase(row.id, {
      assignee: assigneeId
    })

    // 更新本地数据
    row.assignee = assigneeId
    if (assigneeId) {
      const user = assignableUsers.value.find(u => u.id === assigneeId)
      row.assignee_name = user ? user.nickname : ''
    } else {
      row.assignee_name = ''
    }

    ElMessage.success(assigneeId ? '指派成功' : '已取消指派')
  } catch (error) {
    ElMessage.error('指派失败')
  }
}

// 获取可指派用户列表
const fetchAssignableUsers = async () => {
  try {
    const res = await getAssignableUsers()
    assignableUsers.value = res.data || res
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}

// 显示复用用例对话框
const showReuseDialog = () => {
  reuseTestcaseId.value = ''
  reuseDialogVisible.value = true
}

// 复用用例
const handleReuse = async () => {
  if (!reuseTestcaseId.value || !reuseTestcaseId.value.trim()) {
    ElMessage.warning('请输入用例ID')
    return
  }

  reuseLoading.value = true
  try {
    // 获取用例详情
    const res = await getTestcaseDetail(reuseTestcaseId.value.trim())

    // 复制用例信息到表单（排除ID、创建人、创建时间等字段）
    Object.assign(formData, {
      product: res.product || '',
      module: res.module || '',
      sub_module: res.sub_module || '',
      test_point: res.test_point || '',
      title: res.title ? `${res.title} (复制)` : '',
      description: res.description || '',
      precondition: res.precondition || '',
      steps: res.steps || '',
      expected_result: res.expected_result || '',
      actual_result: res.actual_result || '',
      severity: res.severity || 'medium',
      priority: res.priority || 'medium',
      status: 'draft', // 复用的用例默认为草稿状态
      stage: res.stage || null,
      reproduce_steps: res.reproduce_steps ? JSON.parse(JSON.stringify(res.reproduce_steps)) : [],
      case_type: res.case_type || '',
      remark: res.remark || '',
      assignee: null // 不复制指派人员
    })

    ElMessage.success('用例信息已复制到表单，请修改后保存')
    reuseDialogVisible.value = false
  } catch (error) {
    if (error.response?.status === 404) {
      ElMessage.error('用例ID不存在，请检查后重试')
    } else {
      ElMessage.error('复用失败，请检查用例ID是否正确')
    }
  } finally {
    reuseLoading.value = false
  }
}

onMounted(() => {
  fetchList()
  fetchAssignableUsers()
})
</script>

<style scoped>
.testcases-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
  padding: 16px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  margin-bottom: 16px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

.table-card {
  margin-bottom: 20px;
}

.expand-content {
  padding: 16px;
  line-height: 1.8;
}

.expand-content p {
  margin: 8px 0;
}

.import-tips {
  margin-bottom: 16px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.import-tips p {
  margin: 4px 0;
  color: #606266;
}

:deep(.el-pagination) {
  margin-top: 20px;
  justify-content: flex-end;
}

/* 已关闭状态行 - 蓝色高亮 */
:deep(.row-closed td) {
  background-color: #e6f4ff !important;
}
:deep(.row-closed:hover td) {
  background-color: #bae0ff !important;
}

/* 已废弃状态行 - 灰色置灰 */
:deep(.row-deprecated td) {
  background-color: #f5f5f5 !important;
  color: #aaa !important;
}
:deep(.row-deprecated:hover td) {
  background-color: #ebebeb !important;
}
:deep(.row-deprecated .el-link) {
  color: #aaa !important;
}
:deep(.row-deprecated .el-tag) {
  opacity: 0.6;
}

/* 复现步骤编辑器样式 */
.reproduce-steps-editor {
  width: 100%;
}

.steps-list {
  margin-top: 16px;
}

.step-item {
  margin-bottom: 16px;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #f5f7fa;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.step-number {
  font-weight: 600;
  color: #409eff;
}

.step-actions {
  display: flex;
  gap: 8px;
}

.image-upload-area {
  margin-top: 8px;
}

.upload-placeholder {
  text-align: center;
  padding: 20px;
}

.uploaded-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 4px;
  cursor: pointer;
}

.empty-steps {
  margin-top: 16px;
}

/* 复现步骤查看器样式 */
.reproduce-steps-viewer {
  max-height: 500px;
  overflow-y: auto;
}

.step-viewer-item {
  margin-bottom: 16px;
  padding: 12px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background: #fafafa;
}

.step-viewer-header {
  font-weight: 600;
  color: #409eff;
  margin-bottom: 8px;
}

.step-text-content {
  line-height: 1.6;
  color: #606266;
  white-space: pre-wrap;
}

.step-image-content {
  text-align: center;
}

.step-thumbnail {
  max-width: 200px;
  max-height: 150px;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
}

.step-thumbnail:hover {
  transform: scale(1.05);
}

/* 图片放大查看 */
.image-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: pointer;
}

.enlarged-image {
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}
</style>
