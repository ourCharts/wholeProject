<template>
  <div>
    <div id="bottomLeftChart" style="width:100%;height:450px;"></div>
  </div>
</template>

<script>
const echarts = require("echarts");
export default {
  data() {
    return {
      myChart: null,
      delta_guest: [],
      proportion: [],
      time_series: []
    };
  },
  computed: {
    option: function() {
      return {
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(255,255,255,0.1)",
          axisPointer: {
            type: "shadow",
            label: {
              show: true,
              backgroundColor: "#7B7DDC"
            }
          }
        },
        legend: {
          data: ["订单:的士", "提高运载量"],
          textStyle: {
            color: "#B4B4B4",
            fontSize :23
          },
          top: "0%"
        },
        dataZoom: {
          show: false,
          start: 0,
          end: 100
        },
        xAxis: [
          {
            type: "category",
            boundaryGap: true,
            data: this.time_series,
            axisLine: {
              lineStyle: {
                color: "#B4B4B4"
              }
            },
            nameTextStyle: {
              fontSize: 15
            }
          }
        ],
        yAxis: [
          {
            type: "value",
            scale: true,
            name: "比值",
            max: 2,
            min: 1,
            boundaryGap: [0.2, 0.2],
            splitLine: { show: false },
            axisLine: {
              lineStyle: {
                color: "#B4B4B4"
              }
            },
            axisLabel: {
              formatter: "{value} ",
              textStyle: {
                fontSize: 20 //更改坐标轴文字大小
              }
            },
            nameTextStyle: {
              fontSize: 23
            }
          },
          {
            type: "value",
            scale: true,
            name: "乘客运载增量/人",
            min: 0,
            boundaryGap: [0.2, 0.2],
            splitLine: { show: false },
            axisLine: {
              lineStyle: {
                color: "#B4B4B4"
              }
            },
            axisLabel: {
              formatter: "{value} ",
              textStyle: {
                fontSize: 20 //更改坐标轴文字大小
              }
            },
            nameTextStyle: {
              fontSize: 23
            }
          }
        ],
        series: [
          {
            name: "提高运载量",
            type: "bar",
            yAxisIndex: 1,
            data: this.delta_guest,
            barWidth: 20,
            itemStyle: {
              normal: {
                barBorderRadius: 5,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  { offset: 0, color: "#956FD4" },
                  { offset: 1, color: "#3EACE5" }
                ])
              }
            }
          },
          {
            name: "订单:的士",
            type: "line",
            data: this.proportion,
            smooth: true,
            showAllSymbol: true,
            symbol: "emptyCircle",
            symbolSize: 8,

            yAxisIndex: 0,
            itemStyle: {
              normal: {
                color: "#F02FC2"
              }
            }
          }
        ]
      };
    }
  },
  mounted() {
    this.drawPie();
    this.$bus.on("proportion", data => {
      var processed = data[0] - data[1];
      var non_share = processed - data[2];
      var share = data[2];
      var taxi_num = non_share + share / 2;
      if (this.proportion.length >= 9) this.proportion.shift();
      this.proportion.push(processed / taxi_num);
      let delta_taxi = share / 2;
      if (this.delta_guest.length >= 9) this.delta_guest.shift();
      this.delta_guest.push((delta_taxi * processed) / taxi_num);
      console.log("bar:" + this.delta_guest);
      if (this.time_series.length >= 9) this.time_series.shift();
      this.time_series.push(data[3]);
      this.myChart.setOption(this.option);
    });
  },
  methods: {
    drawPie() {
      this.myChart = echarts.init(document.getElementById("bottomLeftChart"));
      this.myChart.setOption(this.option);
      // -----------------------------------------------------------------
      // 响应式变化
      window.addEventListener("resize", () => this.myChart.resize(), false);
    }
  },
  deforeDestroyed() {
    this.$bus.off("proportion");
  },
  destroyed() {
    window.onresize = null;
  }
};
</script>

<style lang="scss" scoped>
</style>