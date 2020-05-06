<template>
  <div ref="map" id="map-container" style="width:500px;height:450px;"></div>
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
        [104.06, 30.65918619836269],
        [104.07, 30],
        [104.027, 30.666259],
        [104.0235, 30.662349],
        [104.06, 30.6622519],
        [104.07, 30.66629],
        [104.0256, 30.662519],
        [104.0537, 30.66429],
        [104.0355, 30.66249],
        [104.0236, 30.6652629],
        [104.05, 30.66249],
        [104.0536, 30.666432519],
        [104.07, 30.66629],
        [104.055, 30.6646249],
        [104.06, 30.662519],
        [104.207, 30.6673629],
        [104.05, 30.66249],
        [104.506, 30.6682519],
        [104.307, 30.666629],
        [104.05, 30.66249],
        [104.506, 30.6625139],
        [104.07, 30.666229],
        [104.025, 30.6446249],
        [104.016, 30.662519],

        [104.046, 31],
        [104.06, 30.6689],
        [104.07, 30.6489],
        [104.03, 30.6589],

        [104.06, 30.6979],
        [104.07, 30.65389],

        [104.06, 30.73619836269]
      ]
    };
  },
  computed: {
    options: function() {
      return {
        animation: true,
        bmap: {
          center: this.centerCoords,
          zoom: 14,
          roam: true
        },
        visualMap: {
          show: false,
          top: "top",
          min: 0,
          max: 5,
          seriesIndex: 0,
          calculable: true,
          inRange: {
            color: ["blue", "blue", "green", "yellow", "red"]
          }
        },
        series: [
          {
            type: "heatmap",
            coordinateSystem: "bmap",
            data: this.busLines,
            pointSize: 10,
            blurSize: 20
          },
          {
            type: "scatter",
            coordinateSystem: "bmap",
            symbol:
              "path://M512 959.469288c-10.69969 0-16.60519-1.283226-20.36584-5.689582-2.261507-2.64934-229.644237-272.535093-290.237267-403.232784-21.890566-46.818305-33.44267-97.655134-33.44267-147.265018 0-187.090049 154.331971-339.226005 344.045777-339.226005s344.045777 153.187915 344.045777 341.429183c0 56.871265-10.660804 99.841939-36.789904 148.300604C747.006362 687.675068 534.795169 950.618713 532.675902 953.24247c-2.532683 3.166109-7.055696 6.227842-20.145829 6.227842L512 959.470311zM512 272.403087c-72.959685 0-132.325771 59.365062-132.325771 132.325771S439.040315 537.054629 512 537.054629s132.325771-59.365062 132.325771-132.325771S584.959685 272.403087 512 272.403087z",
            symbolSize: 50,
            itemStyle: {
              color: "#1A5CD7"
            },
            data: [[104.06, 30.65918619836269]]
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
      // bmap.addControl(new BMap.NavigationControl());
      var goodsData = require("../assets/scss/heat_map.json");
      bmap.setMapStyleV2({
        styleJson: goodsData
      });
      this.mapContorller = bmap;
    }
  },
  mounted() {
    this.$bus.on("heat", data => {
      var random = [];
      for(var i = 0 ; i<data.length;i++)
        if(Math.random()<0.3)
          random.push(data[i]);
      for(var i = 0 ; i<5;i++){
        if(this.busLines.length>3)
          this.busLines.shift();
      }
      this.busLines = this.busLines.concat(random);
      this.chart.setOption(this.options);
    });
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
