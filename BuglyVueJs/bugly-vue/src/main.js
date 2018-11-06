import Vue from 'vue'
import App from './App.vue'
import './plugins/element.js'
import axios from 'axios'
import VCharts from 'v-charts'

Vue.config.productionTip = false



Vue.prototype.$http = axios

Vue.prototype.$http.emulateJSON = true


Vue.use(VCharts)

new Vue({
  render: h => h(App)
}).$mount('#app')
