<template>
  <div class="sidebar-container">
    <el-menu
      :default-active="activeMenu"
      :collapse-transition="false"
      :unique-opened="false"
      :collapse="isCollapse"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      mode="vertical"
    >
      <el-menu-item index="/" @click="handleMenuItemClick('/')">
        <i class="el-icon-s-home" />
        <span slot="title">仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/testcases" @click="handleMenuItemClick('/testcases')">
        <i class="el-icon-document" />
        <span slot="title">测试用例管理</span>
      </el-menu-item>
      <el-menu-item index="/settings" @click="handleMenuItemClick('/settings')">
        <i class="el-icon-setting" />
        <span slot="title">设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Sidebar',
  computed: {
    activeMenu() {
      const route = this.$route
      const { meta, path } = route
      // if set path, the sidebar will highlight the path you set
      if (meta.activeMenu) {
        return meta.activeMenu
      }
      return path
    },
    isCollapse() {
      return !this.$store.state.app.sidebar.opened
    }
  },
  methods: {
    handleMenuItemClick(path) {
      this.$router.push(path)
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebar-container {
  transition: width 0.28s;
  width: 210px !important;
  background-color: #304156;
  height: 100%;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1001;
  overflow: hidden;

  .el-menu {
    border: none;
    height: 100%;
    width: 100% !important;
  }
}

.hideSidebar {
  .sidebar-container {
    width: 54px !important;
  }
}
</style>