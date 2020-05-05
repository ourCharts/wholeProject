import Vue from 'vue'
import Router from 'vue-router'
import index from '@/components/index'
import Map from '@/components/map_origin'
import heat from '@/components/heat'
// import bottomLeft from '@/components/display/bottomLeft'
Vue.use(Router)

export default new Router({
  routes: [
    // {
    //   path:'/debug',
    //   name:'bl',
    //   component:bottomLeft
    // },
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
