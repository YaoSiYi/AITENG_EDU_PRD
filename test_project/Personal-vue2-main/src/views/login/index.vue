<template>
  <div class="login-container">
    <el-form
      v-if="step === 'password'"
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">Testing Performance Platform</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <i class="el-icon-user" />
        </span>
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <i class="el-icon-lock" />
        </span>
        <el-input
          :key="passwordType"
          ref="password"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <i :class="passwordType === 'password' ? 'el-icon-view' : 'el-icon-hide'" />
        </span>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width: 100%; margin-bottom: 30px"
        @click.native.prevent="handleLogin"
      >Login</el-button>
    </el-form>

    <!-- 2FA 验证码输入 -->
    <el-form
      v-else
      ref="form2FA"
      :model="form2FA"
      :rules="rules2FA"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">Google 验证器</h3>
        <p class="tip">请输入 6 位动态验证码</p>
      </div>

      <el-form-item prop="code">
        <span class="svg-container">
          <i class="el-icon-mobile-phone" />
        </span>
        <el-input
          ref="codeInput"
          v-model="form2FA.code"
          placeholder="6 位验证码"
          name="code"
          type="text"
          maxlength="6"
          tabindex="1"
          auto-complete="off"
          @keyup.enter.native="handle2FAVerify"
        />
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width: 100%; margin-bottom: 10px"
        @click.native.prevent="handle2FAVerify"
      >验证</el-button>
      <el-button
        type="text"
        style="width: 100%;"
        @click.native.prevent="step = 'password'"
      >返回</el-button>
    </el-form>
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct username'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    const validate2FACode = (rule, value, callback) => {
      if (!value || !/^\d{6}$/.test(value)) {
        callback(new Error('请输入 6 位数字验证码'))
      } else {
        callback()
      }
    }
    return {
      step: 'password',
      tempToken: '',
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, trigger: 'blur', validator: validateUsername }
        ],
        password: [
          { required: true, trigger: 'blur', validator: validatePassword }
        ]
      },
      form2FA: { code: '' },
      rules2FA: {
        code: [{ required: true, trigger: 'blur', validator: validate2FACode }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          this.loading = true
          this.$store
            .dispatch('user/login', this.loginForm)
            .then((result) => {
              if (result && result.require2fa && result.tempToken) {
                this.tempToken = result.tempToken
                this.step = '2fa'
                this.loading = false
                this.$nextTick(() => {
                  this.$refs.codeInput && this.$refs.codeInput.focus()
                })
                return
              }
              setTimeout(() => {
                this.$router.replace({ path: this.redirect || '/' }).catch(() => {})
                this.loading = false
              }, 100)
            })
            .catch((error) => {
              this.$message.error(error.message || 'Login failed')
              this.loading = false
            })
        } else {
          return false
        }
      })
    },
    handle2FAVerify() {
      this.$refs.form2FA.validate((valid) => {
        if (!valid) return
        this.loading = true
        this.$store
          .dispatch('user/loginWith2FA', {
            tempToken: this.tempToken,
            code: this.form2FA.code
          })
          .then(() => {
            setTimeout(() => {
              this.$router.replace({ path: this.redirect || '/' }).catch(() => {})
              this.loading = false
            }, 100)
          })
          .catch((error) => {
            this.$message.error(error.message || '验证失败')
            this.loading = false
          })
      })
    }
  }
}
</script>

<style lang="scss">
/* Fix input background inconsistency and cursor color */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* Reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      // -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
    font-size: 18px;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }

    .tip {
      font-size: 14px;
      color: $dark_gray;
      margin: -30px auto 30px;
      text-align: center;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
</style>
