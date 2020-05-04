<template>
  <div id="app" style="margin:0">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  }

}
</script>

<style>
  html,
  body {
    height: 100%;
    width: 100%;
    margin: 0;
  }
  .anchorBL {
    display: none;
  }
  .el-header {
    text-align: left;
    font-weight: bolder;
    font-size: 150%;
    letter-spacing: 2px;
    font-family: Impact, Haettenschweiler, ‘Arial Narrow Bold’, sans-serif;
  }
  .el-header, .el-footer {
      background-color: #2F4050;
      color: #9e7d60ff;
      line-height: 10vh;
      border-radius: 10px;
      height: 10% !important;
  }
  .el-aside{
    background-color: rgb(65, 81, 95);
    border-radius: 10px;
    padding: 10px;
    width: 23% !important;
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
