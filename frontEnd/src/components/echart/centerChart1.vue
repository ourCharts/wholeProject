<template>
  <div>
    <div id="centerChart1" style="width:500px;height:400px"></div>
  </div>
</template>

<script>
const echarts = require("echarts");
export default {
  name: "tmp",
  data() {
    return {
      myChart: null,
      share: 0,
      fail: 0,
      order_processed: 0,
    };
  },
  computed: {
    non_share:function () {
      return this.order_processed - this.share;
    },
    data_king: function() {
      return [
        { value: this.share, name: "拼车" },
        { value: this.non_share, name: "独享" },
        { value: this.fail, name: "接单失败" }
      ];
    },
    option: function() {
      return {
        backgroundColor: "rgba(0,0,0,0)",
        tooltip: {
          trigger: "item",
          formatter: "{b}: <br/>{c} ({d}%)"
        },
        color: ["#1A5CD7", "#4ac7f5", "#ac89ff"],
        legend: {
          //图例组件，颜色和名字
          x: "73%",
          y: "center",
          orient: "vertical",
          itemGap: 12, //图例每项之间的间隔
          itemWidth: 15,
          itemHeight: 15,
          icon: "rec",
          data: ["拼车", "独享", "接单失败"],
          textStyle: {
            color: 'rgba(255,255,255,0.8)',
            fontStyle: "normal",
            fontFamily: "微软雅黑",
            fontSize: 28
          }
        },
        series: [
          {
            name: "行业占比",
            type: "pie",
            minAngle: 20, //最小的扇区角度（0 ~ 360）
            center: ["35%", "50%"], //饼图的中心（圆心）坐标
            radius: [100, 150], //饼图的半径
            avoidLabelOverlap: true, ////是否启用防止标签重叠
            itemStyle: {
              //图形样式
              normal: {
                borderColor: "#1e2239",
                borderWidth: 2
              }
            },
            label: {
              //标签的位置
              normal: {
                show: true,
                position: "inside", //标签的位置
                formatter: "{d}%",
                textStyle: {
                  color: "#fff",
                  fontSize: 20
                }
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontWeight: "bold"
                }
              }
            },
            data: this.data_king
          },
          {
            name: "",
            type: "pie",
            silent: true,
            minAngle: 20, //最小的扇区角度（0 ~ 360）
            center: ["35%", "50%"], //饼图的中心（圆心）坐标
            radius: [0, 80], //饼图的半径
            itemStyle: {
              //图形样式
              normal: {
                borderColor: "#1e2239",
                borderWidth: 1.5,
                opacity: 0.21
              }
            },
            label: {
              //标签的位置
              normal: {
                show: false
              }
            },
            data: this.data_king
          }
        ]
      };
    }
  },
  mounted() {
    this.$bus.on("order_finished", data => {
      this.fail = data[2];
      this.order_processed = data[1] - data[2]
      this.myChart.setOption(this.option);
    });
    this.$bus.on("type_of_share_true", data => {
      this.share+=2;
      this.myChart.setOption(this.option);
    });
    this.drawPie();
  },
  beforeDestroy() {
    this.$bus.off("order_finished");
    this.$bus.off("num_of_non_empty_taxi");
  },
  methods: {
    drawPie: function() {
      this.myChart = echarts.init(document.getElementById("centerChart1"));

      // 使用刚指定的配置项和数据显示图表。
      this.myChart.setOption(this.option);
      var _this = this;
      window.addEventListener("resize", function() {
        _this.myChart.resize();
      });
    }
  },
  destroyed() {
    window.onresize = null;
    //window.addEventListener("resize", () => myChartPieLeft.resize(), false);
  }
};
</script>

<style lang="scss" scoped>
</style>