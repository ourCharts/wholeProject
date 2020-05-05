// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {decoration10, loading, decoration8, decoration6, decoration5,borderBox13
  ,borderBox10,borderBox8, borderBox12, decoration2, scrollBoard,scrollRankingBoard} from '@jiaminghi/data-view'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/index.js'
// 引入全局css
import './assets/scss/style.scss'
Vue.use(decoration10);
Vue.use(decoration2);
Vue.use(loading);
Vue.use(decoration8);
Vue.use(decoration5);
Vue.use(decoration6);
Vue.use(borderBox12);
Vue.use(borderBox10);
Vue.use(borderBox8);
Vue.use(borderBox13);
Vue.use(scrollRankingBoard);
Vue.use(scrollBoard);

// 全局注册图标
Vue.component('icon', Icon)

Vue.config.productionTip = false

import VueBus from './router/vue_bus'
Vue.use(VueBus)
// Vue.prototype.$message = Message

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
