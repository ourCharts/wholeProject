<template>
  <div id="app">
    <el-container style="height: 100%">
        <el-header>Header</el-header>
        <el-container>
          <el-aside><amenu @added="changePro" @order="sendId"></amenu></el-aside>
          <el-container>
            <el-main>
              <Map :prop1=xx :prop2=yy :prop3=orderid ></Map>
            </el-main>
            <el-footer>
              footer
            </el-footer>
          </el-container>
        </el-container>
    </el-container>
  </div>
</template>

<script>
import Map from './components/map'
import amenu from './components/menu'
export default {
  name: 'App',
  data () {
    return {
      xx: 'asd',
      yy: 'king',
      orderid: ''
    }
  },
  methods: {
    changePro: function (data1, data2) {
      this.xx = data1
      this.yy = data2
    },
    sendId: function (data3) {
      this.orderid = data3
    }
  },
  components: {
    Map, amenu
  }

}
</script>

<style>
  html,
  body {
    height: 100%;
    width: 100%;
    margin: 0;
    background-color: #3F444C;
  }

  .anchorBL {
    display: none;
  }

  .el-header, .el-footer {
      background-color: #2F4050;
      color: #9e7d60ff;
      text-align: center;
      line-height: 60px;
      border-radius: 10px;
    }
  .el-aside{
    background-color: #41515F;
    border-radius: 10px;
    padding: 10px;
    width: 30% !important;
  }
  #app {
    width: 100%;
    height: 100%;
    margin: 0;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
