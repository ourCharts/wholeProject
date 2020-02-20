<template>
  <el-container>
    <el-main>
      <div ref="map" id="map-container"></div>
    </el-main>
    <el-aside v-loading="loading" element-loading-text="载入路径中.." 
    element-loading-spinner="el-icon-loading" element-loading-background="rgba(65, 81, 95, 0.6)"> 
      <i class="el-icon-edit-outline" id="diy"></i>
      <el-row type="flex" justify="center">
        <el-button type="warning" v-on:click="backCenter">回到原中心位置</el-button>
      </el-row>
      <!-- <el-row type="flex">
        <el-input v-model="input1"></el-input>
        <el-input v-model="input2"></el-input>
        <el-button type="warning" disabled="disabled">自定义添加点</el-button>
      </el-row> -->
      <el-row type="flex">
        <!-- <el-input v-model="input4"></el-input> -->
        <el-input-number v-model="input4" :step="5" :min="5" controls-position="right"></el-input-number>
        <el-button type="warning" v-on:click="addDIY">添加order</el-button>
      </el-row>
      <el-row type="flex">
        <el-input v-model="input3" placeholder="Order_id"></el-input>
        <el-button type="warning" v-on:click="addOne">添加订单路径</el-button>
      </el-row>
      <i class="el-icon-document" id="diy"></i>
      <el-row>
        <el-tag v-for="x in pageArr" :key="x.num" closable type="warning" @close="handleClose(x)" :disable-transitions="true" size="small"> {{x.num}}.{{x.order_id}} </el-tag>
      </el-row>
      <el-row type="flex" justify="center">
        <!-- <el-button type="warning" v-on:click="nextPage(-1)">上一页</el-button> -->
<el-pagination v-show="totalPage" id="fenye"
  layout="prev, pager, next" small
  :page-count="totalPage" :pager-count="5"
  @prev-click="nextPage(-1)" @current-change="goPage"
  @next-click="nextPage(1)">
</el-pagination>
      </el-row>
        <el-row type="flex" justify="center">
          <el-button type="warning" v-on:click="clearPage()" v-show="totalPage">清空</el-button>
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
      loading: false,
      dataset: [],
      displayeID: [],
      arr: [],
      input1: 120,
      input2: 30,
      input3: '39a096b71376b82f35732eff6d95779b',
      input4: 10,
      centerCoords: [],
      page: 0,
      pathNum: 0
    }
  },
  computed: {
    totalPage: function () {
      if (this.dataset.length > 0) return Math.ceil(this.dataset.length / 7.0)
      return null
    },
    pageArr: function () {
      var p = this.page
      let tmpset = this.dataset
      tmpset.sort(function (a, b) {
        return a.num - b.num
      })
      let len = tmpset.length
      if (len > 0) {
        if ((p + 1) * 7 > len) return tmpset.slice(p * 7, len)
        return tmpset.slice(p * 7, (p + 1) * 7)
      } else return null
    },
    options: function () {
      return {
        bmap: {
          center: this.centerCoords,
          zoom: 14,
          roam: true
        },
        series: [{
          type: 'lines',
          coordinateSystem: 'bmap',
          data: this.dataset,
          polyline: true,
          lineStyle: {
            width: 0
          },
          effect: {
            constantSpeed: 80,
            show: true,
            trailLength: 1,
            symbolSize: 6
          }
          // zlevel: 1
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
    backCenter: function () {
      this.centerCoords = [104.08769817540933, 30.70018619836269]
      this.chart.setOption(this.options)
    },
    addOne: function () {
      this.getOrder(this.input3)
    },
    nextPage: function (aa) {
      if (this.totalPage === null) return
      this.page += aa
      if (this.page === -1) this.page = this.totalPage
      if (this.page === this.totalPage) this.page = 0
    },
    goPage: function (val) {
      this.page = val - 1
    },
    changeColor: function () {
      var r = Math.round(105 + 150 * Math.random()).toString(16)
      var g = Math.round(105 + 150 * Math.random()).toString(16)
      var b = Math.round(105 + 150 * Math.random()).toString(16)
      return '#' + r + g + b
    },
    handleClose: function (x) {
      this.dataset.splice(this.dataset.indexOf(x), 1)
      this.chart.setOption(this.options)
      this.pathNum--
    },
    clearPage: function () {
      this.dataset = []
      this.chart.setOption(this.options)
      this.pathNum = 0
    },
    addDIY: function () {
      var tt = this.input4
      // for (let i = 0; i < tt; i++) {
      //   this.getOrder(this.arr[Math.ceil(Math.random() * this.arr.length)])
      // }
      this.loading = true
      var _this = this
      const promises = this.arr.slice(0, tt).map(function (id) {
        return _this.middleFunc(id)
      })
      Promise.all(promises).then(() => {
        console.log('king you are good')
        _this.loading = false
      })
    },
    middleFunc: function (id) {
      var _this = this
      var p = new Promise(function (resolve, reject) {
        _this.getOrder(id, resolve)
      })
      return p
    },
    getOrder: function (newid, resolve) {
      console.log('center is ' + this.centerCoords)
      console.log('getting from server king')
      var _color = this.changeColor()
      this.pathNum++
      var tmpObj = {
        zlevel: Math.ceil(Math.random() * 100),
        order_id: newid,
        num: this.pathNum,
        display: true,
        coords: [],
        lineStyle: {
          normal: {
            color: _color
          }
        }
      }
      let _this = this
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/track_onetime/',
        data: {order_id: newid},
        async: true,
        success: function (response) {
          var obj = response
          var len = obj.length
          var tmparr = []
          for (let i = 0; i < len; i++) {
            tmparr.push([obj[i].longitude, obj[i].latitude])
          }
          tmpObj.coords = tmparr
          console.log(tmpObj)
          _this.dataset.push(tmpObj)
          _this.chart.setOption(_this.options)
          resolve('ok')
        }
      })
    },
    init: function () {
      this.chart = echarts.init(this.$refs.map)
      this.centerCoords = [104.08769817540933, 30.70018619836269]
      this.chart.setOption(this.options)
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.NavigationControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
      var _this = this
      bmap.addEventListener('dragend', function () {
        var obj = bmap.getCenter()
        _this.centerCoords = [obj.lng, obj.lat]
        console.log('hello' + _this.centerCoords)
      })
      // 获得订单order
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/all_id/',
        async: true,
        success: function (response) {
          var obj = response
          var len = obj.length
          for (let i = 0; i < len; i++) { // 记得改200！！！
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
    margin-bottom: 10px
  }
  .el-row{
    margin-bottom: 10px
  }
  .loading{
    color:red
  }
  .el-tag{
    margin-bottom: 6px;
    background-color: #2F4050!important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important;
    font-size: 10px;
    height: 8% !important
  }
  .el-pagination .btn-next, .el-pagination .btn-prev, .el-dialog, .el-pager li, .el-input-number__decrease, .el-input-number__increase{
    background-color: #2F4050!important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important;
  }
   .el-input__inner{
    background-color: #3F444C !important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important;
  }
  .el-input__inner:focus{
    border-color: white !important
  }
  .el-button{
    margin-top: 0px !important;
    padding: 5px !important
  }
  .el-button,.el-button:focus{
    background-color: #2F4050 !important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important
  }
  .el-button:hover, .el-input-number__decrease:hover, .el-input-number__increase:hover, .el-tag:hover{
    background-color: #3F444C !important;
    color: #9e7d60ff;
    border-color: #9e7d60ff
  }
  .el-loading-spinner .el-loading-text, .el-icon-loading:before{
    color: #9e7d60ff !important;

  }
</style>
