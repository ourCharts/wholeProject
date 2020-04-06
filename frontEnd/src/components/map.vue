<template>
    <el-container>
        <el-main>
            <div ref="map" id="map-container"></div>
        </el-main>
        <el-aside v-loading="loading" element-loading-text="载入路径中.." element-loading-spinner="el-icon-loading"
            element-loading-background="rgba(65, 81, 95, 0.6)">
            <el-tabs v-model="activeName" stretch>
                <el-tab-pane label="操作栏" name="first">
                    <i class="el-icon-edit-outline" id="diy"></i>
                    <!-- <el-row type="flex" justify="center">
                        <el-button type="warning" v-on:click="backCenter">回到原中心位置</el-button>
                    </el-row> -->
                    <!-- <el-row type="flex">
                        <el-input-number v-model="input4" :step="5" :min="5" controls-position="right">
                        </el-input-number>
                        <el-button type="warning" v-on:click="addTest">添加order</el-button>
                    </el-row>
                    <el-row type="flex">
                        <el-input v-model="input3" placeholder="Order_id"></el-input>
                        <el-button type="warning" v-on:click="addOne">添加订单路径</el-button>
                    </el-row> -->
                </el-tab-pane>
                <el-tab-pane label="状态栏" name="second">
                    <i class="el-icon-data-analysis" id="diy"></i>
                    <el-row type="flex">
                       <el-col :span="20"><p class="situationBar">原有路径总数</p></el-col>
                      <el-input v-model="dataset.length" placeholder="Order_id" readonly></el-input>
                    </el-row>
                    <el-row type="flex">
                       <el-col :span="20"><p class="situationBar">优化后总数</p></el-col>
                      <el-input v-model="dataset.length" placeholder="Order_id" readonly></el-input>
                    </el-row>
                    <i class="el-icon-document" id="diy" style="display: inline-block"></i><p class="situationBar1">详细路径ID</p>
                    <el-row>
                        <el-tag v-for="x in pageArr" :key="x.num" closable type="warning" @close="handleClose(x)"
                            :disable-transitions="true" size="small"> {{x.num}}.{{x.order_id}} </el-tag>
                    </el-row>
                    <el-row type="flex" justify="center">
                        <!-- <el-button type="warning" v-on:click="nextPage(-1)">上一页</el-button> -->
                        <el-pagination v-show="totalPage" id="fenye" layout="prev, pager, next" small
                            :page-count="totalPage" :pager-count="5" @prev-click="nextPage(-1)" @current-change="goPage"
                            @next-click="nextPage(1)">
                        </el-pagination>
                    </el-row>
                    <el-row type="flex" justify="center">
                        <el-button type="warning" v-on:click="clearPage()" v-show="totalPage">清空</el-button>
                    </el-row>
                </el-tab-pane>
            </el-tabs>

        </el-aside>
    </el-container>
</template>

<script>
// import $ from 'jquery'
import echarts from 'echarts'
import 'echarts/extension/bmap/bmap.js'
export default {
  name: 'Map',
  data () {
    return {
      chart: echarts.ECharts,
      loading: false,
      activeName: 'first',
      taxi_pos: [],
      request_start_pos: [],
      request_end_pos: [],
      chosen_taxi: [],
      dataset: [],
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
    options: function () {
      return {
        bmap: {
          center: this.centerCoords,
          zoom: 14,
          roam: true
        },
        series: [
          {
            type: 'lines',
            coordinateSystem: 'bmap',
            data: this.dataset,
            polyline: true,
            lineStyle: {
              width:10
            }
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            data: this.dataset[0],
            itemStyle: {
              color: 'green'
            }
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            data: this.taxi_pos,
            itemStyle: {
              color: 'black'
            }
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            symbolSize: 30,
            symbol: 'path://M874.666667 469.333333c17.28 42.666667 42.666667 85.333333 42.666666 128v213.333334c0 27.946667-23.893333 42.666667-64 42.666666s-64-17.28-64-42.666666v-42.666667H234.666667v42.666667c0 25.386667-23.893333 42.666667-64 42.666666s-64-14.72-64-42.666666V597.333333c0-42.666667 25.386667-85.333333 42.666666-128s-64-37.333333-64-64 5.333333-42.666667 42.666667-42.666666h64s30.293333-87.04 42.666667-128 64-64 106.666666-64h341.333334c42.666667 0 94.293333 23.04 106.666666 64s42.666667 128 42.666667 128h64c37.333333 0 42.666667 16 42.666667 42.666666s-81.28 21.333333-64 64z m-469.333334 149.333334a21.333333 21.333333 0 0 0 21.333334 21.333333h170.666666a21.333333 21.333333 0 0 0 21.333334-21.333333v-21.333334a21.333333 21.333333 0 0 0-21.333334-21.333333h-170.666666a21.333333 21.333333 0 0 0-21.333334 21.333333v21.333334zM192 618.666667a64 64 0 1 0 64-64 64 64 0 0 0-64 64z m597.333333-256c0-21.333333-42.666667-106.666667-42.666666-106.666667H277.333333s-42.666667 85.333333-42.666666 106.666667v21.333333a42.666667 42.666667 0 0 0 42.666666 42.666667h469.333334a42.666667 42.666667 0 0 0 42.666666-42.666667v-21.333333z m-21.333333 192a64 64 0 1 0 64 64 64 64 0 0 0-64-64z',
            data: this.chosen_taxi,
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            symbolSize: 30,
            symbolKeepAspect: true,
            symbol: 'path://M744.7 417.4v189.1c0 12.1-4.2 22.5-12.7 30.9-8.5 8.5-18.8 12.7-30.9 12.7-12.1 0-22.5-4.2-30.9-12.7-8.5-8.5-12.7-18.7-12.7-30.9v-160h-29.1V861c0 14-5 25.9-15 35.9s-22 15-35.9 15c-14 0-25.9-5-35.9-15s-15-22-15-35.9V650.1h-29.1V861c0 14-5 25.9-15 35.9s-22 15-35.9 15-25.9-5-35.9-15-15-22-15-35.9V446.5h-29.1v160c0 12.1-4.2 22.5-12.7 30.9-8.5 8.5-18.8 12.7-30.9 12.7-12.1 0-22.5-4.2-30.9-12.7-8.5-8.5-12.7-18.7-12.7-30.9V417.4c0-24.3 8.5-44.8 25.4-61.9 16.9-16.9 37.6-25.4 61.9-25.4h290.9c24.3 0 44.8 8.5 61.9 25.4 16.8 17 25.2 37.7 25.2 61.9zM584.1 141.7c19.9 19.9 29.7 43.9 29.7 72.1s-9.9 52.2-29.7 72.1c-19.9 19.9-43.9 29.7-72.1 29.7-28.2 0-52.2-9.9-72.1-29.7-19.9-19.9-29.7-43.9-29.7-72.1s9.9-52.2 29.7-72.1c19.9-19.9 43.9-29.7 72.1-29.7 28.2 0 52.2 9.8 72.1 29.7z',
            data: this.request_start_pos,
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            symbolSize: 30,
            symbolKeepAspect: true,
            symbol: 'path://M512 959.469288c-10.69969 0-16.60519-1.283226-20.36584-5.689582-2.261507-2.64934-229.644237-272.535093-290.237267-403.232784-21.890566-46.818305-33.44267-97.655134-33.44267-147.265018 0-187.090049 154.331971-339.226005 344.045777-339.226005s344.045777 153.187915 344.045777 341.429183c0 56.871265-10.660804 99.841939-36.789904 148.300604C747.006362 687.675068 534.795169 950.618713 532.675902 953.24247c-2.532683 3.166109-7.055696 6.227842-20.145829 6.227842L512 959.470311zM512 272.403087c-72.959685 0-132.325771 59.365062-132.325771 132.325771S439.040315 537.054629 512 537.054629s132.325771-59.365062 132.325771-132.325771S584.959685 272.403087 512 272.403087z',
            data: this.request_end_pos,
          }
        ]
      }
    }
  },
  methods: {
    clearPage: function () {
      this.dataset = []
      this.chart.setOption(this.options)
      this.pathNum = 0
    },
    after_connect: function () {
      var chatSocket = new WebSocket('ws://localhost:8000/ws/track/')
      var _this = this
      chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data)
        if (data['type'] === 'taxi_pos') {
          _this.taxi_pos = data['content']
          _this.chart.setOption(_this.options)
        }
        else if (data['type'] === 'request_pos') {
          _this.request_start_pos.push(data['content'])
          _this.request_end_pos.push(data['content1'])
          alert('新订单')
          _this.chart.setOption(_this.options)
        }
        else if (data['type'] === 'chosen_taxi') {
          _this.chosen_taxi.push(data['content'])
          _this.taxi_pos = []
          alert('更新位置')
          _this.dataset.push(data['content1'])
          _this.chart.setOption(_this.options)
        }
      }
    },
    init: function () {
      this.chart = echarts.init(this.$refs.map)
      this.centerCoords = [104.06, 30.65918619836269]
      this.chart.setOption(this.options)
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.NavigationControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
      this.after_connect()
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
  .el-tabs__active-bar{
    background-color: #9e7d60ff !important;
  }
  .el-loading-spinner .el-loading-text, .el-icon-loading:before, .el-tabs__item.is-active, .el-tabs__item:hover{
    color: #9e7d60ff !important;
    letter-spacing: 3px;
    font-weight: bolder
  }
  .el-tabs__item{
    color: #9e7d60ff !important;
    letter-spacing: 3px;
  }
  .situationBar{
    color: #9e7d60ff !important;
    line-height: 10px;
    letter-spacing: 2px;
  }
  .situationBar1{
    display: inline-block;
    color: #9e7d60ff !important;
    line-height: 20px;
    letter-spacing: 3px;
  }
</style>
