import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

// Global protection: avoid uncaught navigation promise rejections from router.push/replace
// Vue Router returns a promise for push/replace; when navigation is redirected by guards
// the promise can reject and cause 'Uncaught (in promise) Error: Redirected when going from ...'
// Swallow such rejections by wrapping push/replace to return a handled promise when no
// callbacks are provided. This mirrors common community fixes and keeps component-level
// calls simple and safe.
const originalPush = Router.prototype.push
Router.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
  return originalPush.call(this, location).catch(err => err)
}

const originalReplace = Router.prototype.replace
Router.prototype.replace = function replace(location, onResolve, onReject) {
  if (onResolve || onReject) return originalReplace.call(this, location, onResolve, onReject)
  return originalReplace.call(this, location).catch(err => err)
}
import Layout from '@/layout'

// No permission authentication
export const constantRoutes = [

  // Login
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  // Error page
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  // Dashboard
  {
    redirect: 'noRedirect',
    path: '/',
    component: Layout,
    children: [{
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard/index'),
      meta: { title: 'Dashboard', icon: 'dashboard' }
    }]
  },

  // 测试用例管理
  {
    path: '/testcases',
    component: Layout,
    children: [{
      path: '/testcases',
      name: 'Testcases',
      component: () => import('@/views/Testcases/index'),
      meta: { title: '测试用例管理', icon: 'documentation' }
    }]
  },

  // 设置
  {
    path: '/settings',
    component: Layout,
    children: [{
      path: '/settings',
      name: 'Settings',
      component: () => import('@/views/Settings/index'),
      meta: { title: '设置', icon: 'setting' }
    }]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

let routerInstance = null

// Remove async routes, keep only basic functionality
const createRouter = () => {
  routerInstance = new Router({
    mode: 'hash', // require service support
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRoutes
  })
  return routerInstance
}

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router