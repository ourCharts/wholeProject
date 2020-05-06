<template>
  <div>
    <div id="bottomRightChart" style="width:500px;height:350px;"></div>
  </div>
</template>

<script>
const echarts = require("echarts");
export default {
  data() {
    return {
      myChartPieLeft: null,
      result: 0,
      lineCount:10,
      beginYear: 2018,
      currentYear:2018,
      treeDataURI:
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAA2CAYAAADUOvnEAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA5tJREFUeNrcWE1oE0EUnp0kbWyUpCiNYEpCFSpIMdpLRTD15s2ePHixnj00N4/GoyfTg2fbiwdvvagHC1UQ66GQUIQKKgn1UAqSSFua38b3prPJZDs7s5ufKn0w7CaZ2W/fe9/73kyMRqNB3Nrj1zdn4RJ6du9T2u1a2iHYSxjP4d41oOHGQwAIwSUHIyh8/RA8XeiXh0kLGFoaXiTecw/hoTG4ZCSAaFkY0+BpsZceLtiAoV2FkepZSDk5EpppczBvpuuQCqx0YnkYcVVoqQYMyeCG+lFdaGkXeVOFNu4aEBalOBk6sbQrQF7gSdK5JXjuHXuYVIVyr0TZ0FjKDeCs6km7JYMUdrWAUVmZUBtmRnVPK+x6nIR2xomH06R35ggwJPeofWphr/W5UjPIxq8B2bKgE8C4HVHWvg+2gZjXj19PkdFztY7bk9TDCH/g6oafDPpaoMvZIRI5WyMB/0Hv++HkpTKE0kM+A+h20cPAfN4GuRyp9G+LMTW+z8rCLI8b46XO9zRcYZTde/j0AZm8WGb3Y2F9KLlE2nqYkjFLJAsDOl/lea0q55mqxXcL7YBc++bsCPMe8mUyU2ZIpnCoblca6TZA/ga2Co8PGg7UGUlEDd0ueptglbrRZLLE7poti6pCaWUo2pu1oaYI1CF9b9cCZPO3F8ikJQ/rPpQT5YETht26ss+uCIL2Y8vHwJGpA96GI5mjOlaKhowUy6BcNcgIhDviTGWCGFaqEuufWz4pgcbCh+w0gEOyOjTlTtYYlIWPYWKEsLDzOs+nhzaO1KEpd+MXpOoTUgKiNyhdy5aSMPNVqxtSsJFgza5EWA4zKtCJ2OGbLn0JSLu8+SL4G86p1Fpr7ABXdGFF/UTD4rfmFYFw4G9VAJ9SM3aF8l3yok4/J6IV9sDVb36ynmtJ2M5+CwxTYBdKNMBaocKGV2nYgkz6r+cHBP30MzAfi4Sy+BebSoPIOi8PW1PpCCvr/KOD4k9Zu0WSH0Y0+SxJ2awp/nlwKtcGyHOJ8vNHtRJzhPlsHr8MogtlVtwUU0tSM1x58upSKbfJnSKUR07GVMKkDNfXpzpv0RTHy3nZMVx5IOWdZIaPabGFvfpwpjnvfmJHXLaEvZUTseu/TeLc+xgAPhEAb/PbjO6PBaOTf6LQRh/dERde23zxLtOXbaKNhfq2L/1fAOPHDUhOpIf5485h7l+GNHHiSYPKE3Myz9sFxoJuAyazvwIMAItferha5LTqAAAAAElFTkSuQmCC"
    };
  },
  mounted() {
    this.drawPie();
    
    let _this = this
    this.$bus.on("proportion", data => {
      var processed = data[0] - data[1];
      var non_share = processed - data[2];
      var share = data[2];
      var taxi_num = non_share + share / 2;
      let delta_taxi = share / 2;
      _this.result = ((delta_taxi * processed) / taxi_num).toFixed(2);
      _this.currentYear = Math.round(_this.result)%10+_this.beginYear
      _this.myChartPieLeft.setOption({
        xAxis: {
            name: _this.name
        },
        series: [
          {
            data: _this.makeSeriesData(_this.currentYear)
          },
          {
            data: _this.makeSeriesData(_this.currentYear, true)
          }
        ]
      });
    });
  },
  computed: {
    name: function() {
      return "相当于种了 "+this.result+ " 棵树哦~";
    },
    option: function() {
      return {
        color: ["#555555"],
        xAxis: {
          axisLine: { show: false },
          axisLabel: { show: false },
          axisTick: { show: false },
          splitLine: { show: false },
          name: this.name,
          nameLocation: "middle",
          nameGap: 40,
          nameTextStyle: {
            color: "rgba(255,255,255,0.7)",
            fontSize: 30,
            fontFamily: "Arial",
            lineHeight: 33,
          },
          min: -2800,
          max: 2800
        },
        yAxis: {
          data: this.makeCategoryData(),
          show: false
        },
        grid: {
          top: "center",
          height: 100
        },
        series: [
          {
            name: "all",
            type: "pictorialBar",
            symbol: "image://" + this.treeDataURI,
            symbolSize: [30, 55],
            symbolRepeat: true,
            data: this.makeSeriesData(this.beginYear),
            animationEasing: "elasticOut"
          },
          {
            name: "all",
            type: "pictorialBar",
            symbol: "image://" + this.treeDataURI,
            symbolSize: [30, 55],
            symbolRepeat: true,
            data: this.makeSeriesData(this.beginYear, true),
            animationEasing: "elasticOut"
          }
        ]
      };
    }
  },
  methods: {
    makeCategoryData() {
      var categoryData = [];
      for (var i = 0; i < this.lineCount; i++) {
        categoryData.push(i + "a");
      }
      return categoryData;
    },
    makeSeriesData(year, negative) {
      var r = (year - this.beginYear + 1) * 10;
      var seriesData = [];
      for (var i = 0; i < this.lineCount; i++) {
        var sign = negative
          ? -1 * (i % 3 ? 0.9 : 1)
          : 1 * ((i + 1) % 3 ? 0.9 : 1);
        seriesData.push({
          value: 0,
          value:
            sign *
            (year <= this.beginYear + 1
              ? Math.abs(i - this.lineCount / 2 + 0.5) < this.lineCount / 5
                ? 5
                : 0
              : (this.lineCount - Math.abs(i - this.lineCount / 2 + 0.5)) * r),
          symbolOffset: i % 2 ? ["50%", 0] : null
        });
      }
      return seriesData;
    },
    drawPie() {
      // 基于准备好的dom，初始化echarts实例
      this.myChartPieLeft = echarts.init(
        document.getElementById("bottomRightChart")
      );
      this.myChartPieLeft.setOption(this.option);
      // -----------------------------------------------------------------
      // 响应式变化
      window.addEventListener(
        "resize",
        () => this.myChartPieLeft.resize(),
        false
      );
    }
  },
  destroyed() {
    window.onresize = null;
  }
};
</script>

<style lang="scss" scoped>
</style>