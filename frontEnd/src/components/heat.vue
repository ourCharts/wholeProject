<template>
  <div ref="map" id="map-container"></div>
</template>

<script>
// import $ from 'jquery'
/* eslint-disable */
import echarts from "echarts";

import "echarts/extension/bmap/bmap.js";
export default {
  name: "Heat",
  data() {
    return {
      centerCoords: null,
      busLines: [
        {
          coords: [
            [104.06, 30.65918619836269],
            [104.54, 30.65359836269],
            [104.77, 30.15836269]
          ],
          lineStyle:{
              normal:{
                  color:'rgba(245,24,63,1)'
                  
              }
          }
        }
      ]
    };
  },
  computed: {
    options: function() {
      return {
        bmap: {
          center: this.centerCoords,
          zoom: 14,
          roam: true
        },
        series: [
          {
            type: "lines",
            coordinateSystem: "bmap",
            polyline: true,
            data: this.busLines,
            silent: true,
            lineStyle: {
              opacity: 0.2,
              width: 10
            },
            progressiveThreshold: 500,
            progressive: 200
          },
          {
            type: "lines",
            coordinateSystem: "bmap",
            polyline: true,
            data: this.busLines,
            lineStyle: {
              width: 0
            },
            effect: {
              constantSpeed: 40,
              show: true,
              trailLength: 0.3,
              symbolSize: 10
            },
            zlevel: 1
          }
        ]
      };
    }
  },
  methods: {
    init: function() {
      this.chart = echarts.init(this.$refs.map);
      this.centerCoords = [104.06, 30.65918619836269];
      this.chart.setOption(this.options);
      let bmap = this.chart
        .getModel()
        .getComponent("bmap")
        .getBMap();
      // eslint-disable-next-line
      bmap.addControl(new BMap.NavigationControl());
      var goodsData = require("../assets/scss/custom_map_config.json");
      bmap.setMapStyleV2({
        styleId: "59a80bc22d507e09700207fce541bc16"
      });
      this.mapContorller = bmap;
    }
  },
  mounted() {
    this.init();
  },
  beforeDestroy() {}
};
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
  border-radius: 30px;
  padding-bottom: 25px;
}
</style>
