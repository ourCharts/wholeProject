// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {Container, Progress, Main, Aside, Tabs, TabPane, Row, Input, Col, Tag, Pagination, Button, TableColumn, Table, Header, Loading, Message} from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import dataV from '@jiaminghi/data-view'
import Icon from 'vue-awesome/components/Icon'
import 'vue-awesome/icons/index.js'
// 引入全局css
import './assets/scss/style.scss'
Vue.use(dataV)

// 全局注册图标
Vue.component('icon', Icon)

Vue.config.productionTip = false
Vue.use(Container)
Vue.use(Main)
Vue.use(Aside)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Row)
Vue.use(Input)
Vue.use(Col)
Vue.use(Tag)
Vue.use(Pagination)
Vue.use(Button)
Vue.use(TableColumn)
Vue.use(Table)
Vue.use(Header)
Vue.use(Progress)

Vue.use(Loading.directive)

Vue.prototype.$message = Message

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
