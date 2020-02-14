<template>
  <div ref="map" id="map-container"></div>
</template>

<script>
import $ from 'jquery'
import echarts from 'echarts'
import 'echarts/extension/bmap/bmap.js'
export default {
  name: 'Map',
  props: ['prop1', 'prop2', 'prop3'],
  data () {
    return {
      msg: 'hello',
      chart: echarts.ECharts,
      time: 1,
      timer: null,
      dataset: [{coords: [] }]
    }
  },
  computed: {
    options: function () {
      return {
        bmap: {
          center: [104.08166156238282, 30.73315923493018],
          zoom: 16,
          roam: true
        },
        title: {
          subtext: this.p1,
          left: 'center'
        },
        series: [{
          type: 'lines',
          coordinateSystem: 'bmap',
          data: this.dataset,
          polyline: true,
          lineStyle: {
            color: 'red',
            opacity: 0.6,
            width: 10
          }
        }]
      }
    }
  },
  watch: {
    prop1: function () {
      console.log('prop1 changed, it is ' + this.prop1)
      this.addSpect(this.prop1, this.prop2)
    },
    prop2: function () {
      console.log('prop2 changed, it is ' + this.prop2)
      this.addSpect(this.prop1, this.prop2)
    },
    prop3: function () {
      console.log('prop3 changed, it is ' + this.prop3)
      this.getsth(this.prop3)
    }
  },
  methods: {
    sleep: function (ms) {
      console.log('sleep')
      return new Promise(function (resolve, reject) {
        setTimeout(resolve, ms)
      })
    },
    addSpect: function (x, y) {
      this.dataset[0].coords.splice(0, 0, [x, y])
      this.options.bmap.center = [x, y]
      this.chart.setOption(this.options)
    },
    getsth: function (newid) {
      console.log('getting from server king')
      let _this = this
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.MapTypeControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/track_onetime/',
        data: {order_id: newid},
        async: true,
        success: function (response) {
          var obj = response
          for (let i = 0; i < obj.length; i++) {
            _this.sleep(i * 101).then(function () {
              console.log(obj[i].time_stamp)
              _this.addSpect(obj[i].longitude, obj[i].latitude)
            })
          }
        }
      })
    },
    init: function () {
      this.chart = echarts.init(this.$refs.map)
      this.chart.setOption(this.options)
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.MapTypeControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
    }
  },
  mounted () {
    this.init()
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
  margin: 0;
}
</style>
