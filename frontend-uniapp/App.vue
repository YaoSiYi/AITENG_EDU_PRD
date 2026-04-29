<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
    // 检查登录状态
    const token = uni.getStorageSync('token')
    if (token) {
      this.checkAuth()
    }
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  },
  methods: {
    checkAuth() {
      uni.request({
        url: this.globalData.apiBase + '/users/profile/',
        header: {
          'Authorization': 'Bearer ' + uni.getStorageSync('token')
        },
        success: (res) => {
          if (res.statusCode === 200) {
            this.globalData.userInfo = res.data
          } else {
            uni.removeStorageSync('token')
          }
        }
      })
    }
  },
  globalData: {
    apiBase: 'http://localhost:8000/api',
    userInfo: null
  }
}
</script>

<style>
@import './common/common.css';
</style>
