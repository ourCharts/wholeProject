import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import Map from '@/components/map_origin'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: index
    },
    {
      path:'/map',
      name:'map',
      component:Map
    }
  ],
  mode:'history'
})
