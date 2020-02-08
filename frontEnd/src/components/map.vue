<template>
  <div ref="map" id="map-container"></div>
</template>

<script>
import echarts from 'echarts'
import 'echarts/extension/bmap/bmap.js'
export default {
  name: 'Map',
  props: ['prop1', 'prop2'],
  data () {
    return {
      msg: 'hello',
      chart: echarts.ECharts,
      time: 1,
      timer: null,
      dataset: [
        [120.13066322374, 30.240018034923],
        [120, 30],
        [120, 30.1],
        [119.8, 29.989]
      ]
    }
  },
  computed: {
    options: function () {
      return {
        bmap: {
          center: [120.13066322374, 30.240018034923],
          zoom: 10,
          roam: true
        },
        title: {
          subtext: this.p1,
          left: 'center'
        },
        series: [{
          type: 'scatter',
          coordinateSystem: 'bmap',
          data: this.dataset
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
    }
  },
  methods: {
    addData: function (tmp) {
      this.dataset.push([120, 30.04 + tmp])
    },
    addSpect: function (x, y) {
      this.dataset.push([x, y])
      this.chart.setOption(this.options)
      console.log('asdasdasd')
    },
    addPoint: function () {
      this.addData(0.1 * this.time)
      this.time++
      this.chart.setOption(this.options)
    },
    init: function () {
      console.log(this.prop1 + '**********')
      console.log(this.prop2 + '**********')
      this.chart = echarts.init(this.$refs.map)
      console.log('debug: ' + this.chart)
      this.chart.setOption(this.options)
      let bmap = this.chart.getModel().getComponent('bmap').getBMap()
      // eslint-disable-next-line
      bmap.addControl(new BMap.MapTypeControl())
      bmap.setMapStyleV2({
        styleId: '59a80bc22d507e09700207fce541bc16'
      })
      this.timer = setInterval(this.addPoint, 3000)
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
