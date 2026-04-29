<template>
  <div class="app-container">
    <h2 class="section-title">账户安全</h2>

    <!-- 2FA 状态 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>双因素认证 (2FA)</span>
        <el-tag v-if="statusLoading" type="info" size="small">加载中...</el-tag>
        <el-tag v-else-if="statusEnabled" type="success" size="small">已开启</el-tag>
        <el-tag v-else type="info" size="small">未开启</el-tag>
      </div>
      <div v-loading="statusLoading" class="card-body">
        <template v-if="!statusEnabled && !setupMode">
          <p>开启后，登录时需额外输入 Google 验证器中的 6 位动态码。</p>
          <el-button type="primary" :loading="setupLoading" @click="handleSetupStart">开启 2FA</el-button>
        </template>

        <!-- 设置中：扫码 + 输入验证码确认 -->
        <template v-else-if="setupMode">
          <div v-if="qrUri" class="setup-step">
            <p>1. 使用 Google Authenticator 扫描下方二维码</p>
            <div class="qr-wrap">
              <img :src="qrDataUrl" alt="2FA QR" width="200" height="200">
            </div>
            <p class="mt">2. 输入验证器中显示的 6 位验证码以确认</p>
            <el-input
              v-model="confirmCode"
              placeholder="6 位验证码"
              maxlength="6"
              style="width: 200px; margin-right: 10px;"
              @keyup.enter.native="handleConfirm"
            />
            <el-button type="primary" :loading="confirmLoading" @click="handleConfirm">确认开启</el-button>
            <el-button @click="handleSetupCancel">取消</el-button>
          </div>
        </template>

        <!-- 已开启：关闭 2FA -->
        <template v-else>
          <p>双因素认证已开启，登录时需要验证码。</p>
          <el-button type="danger" plain :loading="disableLoading" @click="showDisable = true">关闭 2FA</el-button>
        </template>
      </div>
    </el-card>

    <!-- 关闭 2FA 对话框 -->
    <el-dialog title="关闭 2FA" :visible.sync="showDisable" width="400px">
      <el-form ref="disableForm" :model="disableForm" :rules="disableRules" label-width="80px">
        <el-form-item label="当前密码" prop="password">
          <el-input v-model="disableForm.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input v-model="disableForm.code" placeholder="6 位验证码" maxlength="6" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="showDisable = false">取消</el-button>
        <el-button type="danger" :loading="disableLoading" @click="handleDisable">确认关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import QRCode from 'qrcode'
import { get2FAStatus, setup2FA, confirm2FA, disable2FA } from '@/api/user'

export default {
  name: 'Settings',
  data() {
    const validateCode = (rule, value, cb) => {
      if (!value || !/^\d{6}$/.test(value)) {
        cb(new Error('请输入 6 位数字验证码'))
      } else {
        cb()
      }
    }
    return {
      statusLoading: false,
      statusEnabled: false,
      setupLoading: false,
      setupMode: false,
      qrUri: '',
      qrDataUrl: '',
      confirmCode: '',
      confirmLoading: false,
      disableLoading: false,
      showDisable: false,
      disableForm: { password: '', code: '' },
      disableRules: {
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        code: [{ required: true, validator: validateCode, trigger: 'blur' }]
      }
    }
  },
  created() {
    this.fetchStatus()
  },
  methods: {
    fetchStatus() {
      this.statusLoading = true
      get2FAStatus()
        .then(res => {
          const data = (res && res.data !== undefined) ? res.data : res
          this.statusEnabled = !!(data && data.enabled)
        })
        .catch(() => {
          this.statusEnabled = false
        })
        .finally(() => {
          this.statusLoading = false
        })
    },
    async handleSetupStart() {
      this.setupLoading = true
      try {
        const res = await setup2FA()
        const data = (res && res.data !== undefined) ? res.data : res
        const uri = data && data.qr_uri
        if (!uri) {
          this.$message.error('获取二维码失败')
          return
        }
        this.qrUri = uri
        this.qrDataUrl = await QRCode.toDataURL(uri)
        this.setupMode = true
      } catch (e) {
        this.$message.error(e.message || '发起设置失败')
      } finally {
        this.setupLoading = false
      }
    },
    handleSetupCancel() {
      this.setupMode = false
      this.qrUri = ''
      this.qrDataUrl = ''
      this.confirmCode = ''
    },
    handleConfirm() {
      if (!this.confirmCode || !/^\d{6}$/.test(this.confirmCode)) {
        this.$message.warning('请输入 6 位验证码')
        return
      }
      this.confirmLoading = true
      confirm2FA(this.confirmCode)
        .then(() => {
          this.$message.success('2FA 已开启')
          this.handleSetupCancel()
          this.statusEnabled = true
        })
        .catch(e => {
          this.$message.error(e.message || '确认失败')
        })
        .finally(() => {
          this.confirmLoading = false
        })
    },
    handleDisable() {
      this.$refs.disableForm.validate(valid => {
        if (!valid) return
        this.disableLoading = true
        disable2FA(this.disableForm.password, this.disableForm.code)
          .then(() => {
            this.$message.success('2FA 已关闭')
            this.showDisable = false
            this.disableForm = { password: '', code: '' }
            this.statusEnabled = false
          })
          .catch(e => {
            this.$message.error(e.message || '关闭失败')
          })
          .finally(() => {
            this.disableLoading = false
          })
      })
    }
  }
}
</script>

<style scoped>
.section-title {
  margin-bottom: 20px;
  font-size: 18px;
}
.box-card {
  max-width: 560px;
}
.card-body p {
  margin-bottom: 12px;
  color: #606266;
}
.setup-step p {
  margin-bottom: 8px;
}
.qr-wrap {
  margin: 16px 0;
  padding: 16px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  display: inline-block;
}
.mt {
  margin-top: 16px;
}
</style>
