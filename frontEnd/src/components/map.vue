<template>
  <div ref="map" id="map-container"></div>
</template>

<script>
// import $ from 'jquery'
/* eslint-disable */
import echarts from "echarts";

import "echarts/extension/bmap/bmap.js";
export default {
  name: "Map",
  data() {
    return {
      // chosen_taxi: [{'value':[[104.06, 30.65918619836269],[104.07, 30.65918619836269]], 'itemStyle': {'color':'white'}}],
      chart: echarts.ECharts,
      taxi_path: [], // 元素是数组A, 每个A里面都装着若干个二维数组（装着坐标）
      all_request_start: [], //所有订单起点 ， 元素是一个二维数组（装着坐标）
      all_request_end: [], //所有订单终点 ， 元素是一个二维数组（装着坐标）
      taxi_path_start: [], // 所有的士 接单时的位置 ， 元素是一个二维数组（装着坐标）
      all_non_empty_taxi: [], // 元素是所有已接单的的士id
      order_finished: [] // 元素是所有已经完成的订单的id
    };
  },
  computed: {
    options: function() {
      return {
        bmap: {
          center: this.centerCoords,
          zoom: 15,
          roam: true
        },
        tooltip: {
          show: true,
          trigger: "item",
          showContent: "true",
          formatter: "{b}\n经纬度：{c}"
        },
        series: [
          {
            type: "lines",
            coordinateSystem: "bmap",
            data: this.taxi_path,
            polyline: true,
            lineStyle: {
              width: 10
            },
            label: {
              show: true,
              position: "start",
              formatter: "起点: {c}",
              backgroundColor: "yellow"
            }
          },
          {
            type: 'scatter',
            coordinateSystem: 'bmap',
            symbol:
              "path://M512 959.469288c-10.69969 0-16.60519-1.283226-20.36584-5.689582-2.261507-2.64934-229.644237-272.535093-290.237267-403.232784-21.890566-46.818305-33.44267-97.655134-33.44267-147.265018 0-187.090049 154.331971-339.226005 344.045777-339.226005s344.045777 153.187915 344.045777 341.429183c0 56.871265-10.660804 99.841939-36.789904 148.300604C747.006362 687.675068 534.795169 950.618713 532.675902 953.24247c-2.532683 3.166109-7.055696 6.227842-20.145829 6.227842L512 959.470311zM512 272.403087c-72.959685 0-132.325771 59.365062-132.325771 132.325771S439.040315 537.054629 512 537.054629s132.325771-59.365062 132.325771-132.325771S584.959685 272.403087 512 272.403087z",
            symbolSize: 50,
            itemStyle:{
              color:'#1A5CD7'
            },
            data: [[104.06, 30.65918619836269]],
        },
          {
            type: "scatter",
            coordinateSystem: "bmap",
            symbolSize: 30,
            symbol:
              "path://M874.666667 469.333333c17.28 42.666667 42.666667 85.333333 42.666666 128v213.333334c0 27.946667-23.893333 42.666667-64 42.666666s-64-17.28-64-42.666666v-42.666667H234.666667v42.666667c0 25.386667-23.893333 42.666667-64 42.666666s-64-14.72-64-42.666666V597.333333c0-42.666667 25.386667-85.333333 42.666666-128s-64-37.333333-64-64 5.333333-42.666667 42.666667-42.666666h64s30.293333-87.04 42.666667-128 64-64 106.666666-64h341.333334c42.666667 0 94.293333 23.04 106.666666 64s42.666667 128 42.666667 128h64c37.333333 0 42.666667 16 42.666667 42.666666s-81.28 21.333333-64 64z m-469.333334 149.333334a21.333333 21.333333 0 0 0 21.333334 21.333333h170.666666a21.333333 21.333333 0 0 0 21.333334-21.333333v-21.333334a21.333333 21.333333 0 0 0-21.333334-21.333333h-170.666666a21.333333 21.333333 0 0 0-21.333334 21.333333v21.333334zM192 618.666667a64 64 0 1 0 64-64 64 64 0 0 0-64 64z m597.333333-256c0-21.333333-42.666667-106.666667-42.666666-106.666667H277.333333s-42.666667 85.333333-42.666666 106.666667v21.333333a42.666667 42.666667 0 0 0 42.666666 42.666667h469.333334a42.666667 42.666667 0 0 0 42.666666-42.666667v-21.333333z m-21.333333 192a64 64 0 1 0 64 64 64 64 0 0 0-64-64z",
            data: this.all_non_empty_taxi
          },
          {
            type: "scatter",
            coordinateSystem: "bmap",
            symbolSize: 30,
            symbolKeepAspect: true,
            symbol:
              "path://M744.7 417.4v189.1c0 12.1-4.2 22.5-12.7 30.9-8.5 8.5-18.8 12.7-30.9 12.7-12.1 0-22.5-4.2-30.9-12.7-8.5-8.5-12.7-18.7-12.7-30.9v-160h-29.1V861c0 14-5 25.9-15 35.9s-22 15-35.9 15c-14 0-25.9-5-35.9-15s-15-22-15-35.9V650.1h-29.1V861c0 14-5 25.9-15 35.9s-22 15-35.9 15-25.9-5-35.9-15-15-22-15-35.9V446.5h-29.1v160c0 12.1-4.2 22.5-12.7 30.9-8.5 8.5-18.8 12.7-30.9 12.7-12.1 0-22.5-4.2-30.9-12.7-8.5-8.5-12.7-18.7-12.7-30.9V417.4c0-24.3 8.5-44.8 25.4-61.9 16.9-16.9 37.6-25.4 61.9-25.4h290.9c24.3 0 44.8 8.5 61.9 25.4 16.8 17 25.2 37.7 25.2 61.9zM584.1 141.7c19.9 19.9 29.7 43.9 29.7 72.1s-9.9 52.2-29.7 72.1c-19.9 19.9-43.9 29.7-72.1 29.7-28.2 0-52.2-9.9-72.1-29.7-19.9-19.9-29.7-43.9-29.7-72.1s9.9-52.2 29.7-72.1c19.9-19.9 43.9-29.7 72.1-29.7 28.2 0 52.2 9.8 72.1 29.7z",
            data: this.all_request_start
          },
          {
            type: "scatter",
            coordinateSystem: "bmap",
            symbolSize: 30,
            symbolKeepAspect: true,
            symbol:
              "path://M512 959.469288c-10.69969 0-16.60519-1.283226-20.36584-5.689582-2.261507-2.64934-229.644237-272.535093-290.237267-403.232784-21.890566-46.818305-33.44267-97.655134-33.44267-147.265018 0-187.090049 154.331971-339.226005 344.045777-339.226005s344.045777 153.187915 344.045777 341.429183c0 56.871265-10.660804 99.841939-36.789904 148.300604C747.006362 687.675068 534.795169 950.618713 532.675902 953.24247c-2.532683 3.166109-7.055696 6.227842-20.145829 6.227842L512 959.470311zM512 272.403087c-72.959685 0-132.325771 59.365062-132.325771 132.325771S439.040315 537.054629 512 537.054629s132.325771-59.365062 132.325771-132.325771S584.959685 272.403087 512 272.403087z",
            data: this.all_request_end
          },
          {
            type: "scatter",
            coordinateSystem: "bmap",
            data: this.taxi_path_start
          }
        ]
      };
    }
  },
  methods: {
    after_connect: function() {
      var chatSocket = new WebSocket("ws://localhost:8000/ws/track/");
      var _this = this;

      // 心跳检测，防止websocket自动断开连接
      let heartCheck = {
        timeout: 60000, // 60s发送一次心跳
        timeoutObj: null,
        serverTimeoutObj: null,
        reset: function() {
          // console.log("reset setTimeOut!");
          clearTimeout(this.serverTimeoutObj);
          clearTimeout(this.timeoutObj);
          return this;
        },
        start: function() {
          this.timeoutObj = setTimeout(() => {
            chatSocket.send("ping");
            // console.log("ping!");
            this.serverTimeoutObj = setTimeout(_ => {
              chatSocket.close();
              // console.log("ws连接已断开！");
            }, this.timeout * 2); // 如果两倍心跳间隔内还未回复说明ws连接已断开
          }, this.timeout);
        }
      };
      chatSocket.onopen = () => {
        heartCheck.reset().start();
        //   console.log("websocket连接成功！");
      };
      chatSocket.onerror = () => {
        heartCheck.reset();
      };
      chatSocket.onmessage = function(e) {
        heartCheck.reset().start(); // 收到服务器任何响应都应重置计时器
        var data = JSON.parse(e.data);
        if (data["type"] === "request_pos") {
          _this.now_time = data["time"];
        } else if (data["type"] === "taxi_path") {
          _this.taxi_path = data["content"];
          _this.$bus.emit("taxi_path", data["content"]);
          _this.chart.setOption(_this.options);
        } else if (data["type"] === "req_to_taxi_map") {
          _this.$bus.emit("req_to_taxi_map", [
            data["order"],
            data["taxi"],
            data["share"]
          ]);
        } else if (data["type"] === "all_request_start") {
          _this.all_request_start = data["content"];
          _this.$bus.emit("heat", data['content'].map(x=>{
            return x['value']
          }));
          _this.chart.setOption(_this.options);
        } else if (data["type"] === "all_request_end") {
          _this.all_request_end = data["content"];
          _this.$bus.emit("heat", data['content'].map(x=>{
            return x['value']
          }));
          _this.chart.setOption(_this.options);
        } else if (data["type"] === "all_non_empty_taxi") {
          _this.all_non_empty_taxi = data["content"];

          _this.chart.setOption(_this.options);
        } else if (data["type"] === "taxi_path_start") {
          _this.taxi_path_start = data["content"];
          _this.chart.setOption(_this.options);
        } else if (data["type"] === "type_of_share_true") {
          _this.$bus.emit("type_of_share_true", "");
        } else if (data["type"] === "order_finished") {
          //alert(data['content'])
          _this.$bus.emit("order_finished", [
            data["content"],
            data["num"],
            data["fail"],
            data["non_empty_taxi"],
            data["time"],
            data["share_or_not"]
          ]);
        }
      };
    },
    init: function() {
      this.chart = echarts.init(this.$refs.map);
      this.centerCoords = [104.06, 30.65918619836269];
      this.chart.setOption(this.options);
      let bmap = this.chart
        .getModel()
        .getComponent("bmap")
        .getBMap();
      // eslint-disable-next-line
      var goodsData = require("../assets/scss/custom_map_config.json");
      bmap.setMapStyleV2({
        // styleId:'f20aa46cedf21b09b47a71d84116c411'
        styleJson: goodsData
      });

      this.after_connect();
    }
  },
  mounted() {
    // setTimeout(() => {
    //   this.$bus.emit(
    //   "taxi_path",
    //   [{
    //       name: 'asd',
    //       value: 13
    //     }]
    // );
    // }, 2000);
    this.init();
  },
  beforeDestroy() {
    // clearInterval(this.timer)
  }
};
</script>

<style>
#map-container {
  width: 100%;
  height: 100%;
  border-radius: 30px;
  padding-bottom: 25px;
}
#diy {
  color: #9e7d60ff;
  font-size: 200%;
  margin-bottom: 10px;
}
</style>
