import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import Map from '@/components/map_origin'
import heat from '@/components/heat'
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
    },
    {
      path:'/heat',
      name:'heat',
      component:heat
    }
  ],
  mode:'history'
})
