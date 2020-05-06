<template>
  <div id="centreRight1">
    <div class="bg-color-black">
      <div style="text-align:center">
        <dv-decoration-11 class="king_subtitle">订单信息</dv-decoration-11>
      </div>
      <div class="d-flex jc-center body-box">
        <dv-scroll-board :config="config" style="width:100%;height:360px" />
      </div>
      <div class="ranking">
        <div style="text-align:center">
          <dv-decoration-11 class="king_subtitle">出租车行程汇报</dv-decoration-11>
        </div>
        <dv-scroll-ranking-board :config="ranking" style="height:280px" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      config_arr: [
        ["正在载入中", "正在载入中", "正在载入中"],
      ],
      ranking: {
        data: [{
          name: '正在载入中',
          value: 0
        }],
        waitTime: 4000,
        unit: "%"
      }
    };
  },
  computed: {
    config: function() {
      return {
        header: ["订单编号", "对应的士", "订单类型"],
        data: this.config_arr,
        rowNum: 7, //表格行数
        headerHeight: 40,
        headerBGC: "#0f1325", //表头
        oddRowBGC: "#0f1325", //奇数行
        evenRowBGC: "#171c33", //偶数行
        index: true,
        columnWidth: [50],
        align: ["center"]
      };
    }
  },
  mounted() {
    this.$bus.on("taxi_path", tmp => {
      var taxi_situation = tmp.map(x => {
        return {
          name: x["name"],
          value: x["ok"]
        };
      });
      var order_to_taxi = [];
      for (var idx = 0; idx < tmp.length; idx++) {
        var taxiId = tmp[idx]["name"].replace("的士编号：", "");
        if (tmp[idx]["guest"].length == 1) {
          order_to_taxi.push([
            tmp[idx]["guest"][0],
            taxiId,
            "<span  class='colorRed'>独享</span>"
          ]);
        } else {
          for (let index = 0; index < tmp[idx]["guest"].length; index++)
            order_to_taxi.push([
              tmp[idx]["guest"][index],
              taxiId,
              "<span  class='colorGrass'>拼车</span>"
            ]);
        }
      }
      this.config_arr = order_to_taxi;
      this.ranking = {
        data: taxi_situation,
        waitTime: 4000,
        unit: "%"
      };
    });
  },
  beforeDestroy() {
    this.$bus.off("taxi_path");
    // this.$bus.off("req_to_taxi_map");
  }
};
</script>

<style lang="scss">
#centreRight1 {
  padding: 1rem;
  height: 410px;
  min-width: 300px;
  border-radius: 5px;
  .bg-color-black {
    height: 385px;
    border-radius: 10px;
  }
  .text {
    color: #c3cbde;
  }
  .body-box {
    border-radius: 10px;
    overflow: hidden;
  }
}
.king_subtitle {
  width: 200px;
  height: 35px;
  margin: auto;
  margin-top: -10px;
  line-height: 20px;
  // margin-bottom: -10px;
  font-size: 1.6rem;
  letter-spacing: 3px;
}
</style>