<template>
  <div>
    <div id="centerChart1" style="width:500px;height:400px"></div>
  </div>
</template>

<script>
const echarts = require("echarts");
export default {
  name:'tmp',
  data() {
    return {
      share: 31,
      non_share:10,
      fail:5
    };
  },
  computed:{
    data_king:function () {
      return [
        { value: this.share, name: "拼车" },
        { value: this.non_share, name: "独享" },
        { value: this.fail, name: "接单失败" }
      ]
    }
  },
  mounted() {
    this.drawPie();
  },
  methods: {
    drawPie: function() {
      var myChart = echarts.init(document.getElementById("centerChart1"));
      var data = this.data_king;
      var option = {
        backgroundColor: "rgba(0,0,0,0)",
        tooltip: {
          trigger: "item",
          formatter: "{b}: <br/>{c} ({d}%)"
        },
        color: ["#1A5CD7", "#4ac7f5", "#0089ff"],
        legend: {
          //图例组件，颜色和名字
          x: "73%",
          y: "center",
          orient: "vertical",
          itemGap: 12, //图例每项之间的间隔
          itemWidth: 10,
          itemHeight: 10,
          icon: "circle",
          data: ["拼车", "独享", "接单失败"],
          textStyle: {
            color: [],
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
                  fontSize:20
                }
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontWeight: "bold"
                }
              }
            },
            data: data
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
            data: data
          }
        ]
      };

      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      window.addEventListener("resize", function() {
        myChart.resize();
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