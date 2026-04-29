import Vue from 'vue'
import 'normalize.css/normalize.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import '@/styles/index.scss'
import App from './App'
import store from './store'
import router from './router'
import '@/permission'
import axios from 'axios'
import VueAxios from 'vue-axios'
import * as echarts from 'echarts'
import watermark from './watermark'


Vue.directive('watermark', {
  bind: function(el, binding) {
    const text = binding.value
    watermark.set(text)
  }
})
/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
// if (process.env.NODE_ENV === 'production') {
//   const { mockXHR } = require('../mock')
//   mockXHR()
// }

// set ElementUI lang to EN
// Vue.use(ElementUI, { locale })

// If you want to use Chinese version of element-ui, declare as follows
Vue.use(ElementUI)
Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios
Vue.use(VueAxios, axios)
Vue.config.productionTip = false


new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
