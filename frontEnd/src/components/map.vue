<template>
  <el-container>
    <el-main>
      <div ref="map" id="map-container"></div>
    </el-main>
    <el-aside>
      <i class="el-icon-edit-outline" id="diy"></i>
      <el-row type="flex">
        <el-input v-model="input1"></el-input>
        <el-input v-model="input2"></el-input>
        <el-button type="warning" disabled="disabled">自定义添加点</el-button>
      </el-row>
      <el-row type="flex">
        <el-input v-model="input4"></el-input>
        <el-button type="warning" v-on:click="addDIY">添加order</el-button>
      </el-row>
      <el-row type="flex">
        <el-input v-model="input3" placeholder="Order_id"></el-input>
        <el-button type="warning" v-on:click="addOne">添加订单路径</el-button>
      </el-row>
      <i class="el-icon-document" id="diy"></i>
      <el-row>
        <el-card class="box-card" shadow="hover" v-for="x in arr" :key="x">{{x}}</el-card>
      </el-row>
    </el-aside>
  </el-container>
</template>

<script>
import $ from 'jquery'
import echarts from 'echarts'
import 'echarts/extension/bmap/bmap.js'
export default {
  name: 'Map',
  data () {
    return {
      chart: echarts.ECharts,
      time: -1,
      dataset: [],
      arr: [],
      input1: 120,
      input2: 30,
      input3: '39a096b71376b82f35732eff6d95779b',
      input4: 4
    }
  },
  computed: {
    options: function () {
      return {
        bmap: {
          center: [104.08166156238282, 30.73315923493018],
          zoom: 13,
          roam: true
        },
        // title: {
        //   subtext: 'hello world',
        //   left: 'center'
        // },
        series: [{
          type: 'lines',
          coordinateSystem: 'bmap',
          data: this.dataset,
          polyline: true,
          lineStyle: {
            color: 'red',
            opacity: 1,
            width: 5
          }
        }]
      }
    }
  },
  methods: {
    sleep: function (ms) {
      return new Promise(function (resolve, reject) {
        setTimeout(resolve, ms)
      })
    },
    addDIY: function () {
      var tt = this.input4
      for (let i = 0; i < tt; i++) {
        this.getOrder(this.arr[i])
      }
    },
    addOne: function () {
      this.getOrder(this.input3)
    },
    addSpect: function (i, x, y) {
      // this.dataset[i].coords.splice(0, 0, [x, y])性能未知
      this.dataset[i].coords.push([x, y])
      this.chart.setOption(this.options)
    },
    getOrder: function (newid) {
      console.log('getting from server king')
      this.time++
      var tmptime = this.time
      var tmpObj = {
        coords: []
      }
      this.dataset.push(tmpObj)
      let _this = this
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/track_onetime/',
        data: {order_id: newid},
        async: true,
        success: function (response) {
          var obj = response
          var len = obj.length
          for (let i = 0; i < len; i++) {
            // _this.sleep(i * 100).then(function () {
            // _this.addSpect(tmptime, obj[i].longitude, obj[i].latitude)
            // console.log(_this.dataset)
            // })
            setTimeout(() => {
              _this.addSpect(tmptime, obj[i].longitude, obj[i].latitude)
            }, i * 100)
          }
        }
      })
    },
    init: function () {
      this.chart = echarts.init(this.$refs.map)
      this.chart.setOption(this.options)
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.NavigationControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
      // 获得订单order
      var _this = this
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/all_id/',
        async: true,
        success: function (response) {
          var obj = response
          for (let i = 0; i < 10; i++) {
            _this.arr.push(obj[i].order_id)
          }
        }
      })
    }
  },
  mounted () {
    this.init()
  },
  beforeDestroy () {
    // clearInterval(this.timer)
  }
}
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
  margin: 0;
  border-radius: 10px;
}
  #diy{
    color: #9e7d60ff;
    font-size: 200%;
    margin-bottom: 20px
  }
  .el-row{
    margin-bottom: 10px
  }
  .el-card{
    margin-bottom: 10px;
    background-color: #2F4050;
    color: #9e7d60ff;
    border-color: #9e7d60ff;
    font-size: 10px;
  }
  .el-card__body{
    padding: 3px !important
  }
   .el-input__inner{
    background-color: #3F444C !important;
    color: #9e7d60ff;
    border-color: #9e7d60ff
  }
  .el-input__inner:focus{
    border-color: white !important
  }
  .el-button{
    padding: 5px !important
  }
  .el-button,.el-button:focus{
    background-color: #2F4050 !important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important
  }
  .el-button:hover{
    background-color: #3F444C !important;
    color: #9e7d60ff;
    border-color: #9e7d60ff
  }
</style>
