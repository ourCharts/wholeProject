<template>
  <div id="centreRight1">
    <div class="bg-color-black">
      <div class="d-flex pt-2 pl-2">
        <span style="color:#5cd9e8">
          <icon name="chart-line"></icon>
        </span>
        <div class="d-flex">
          <span class="fs-xl text mx-2">行程完成程度</span>
        </div>
      </div>
      <div class="d-flex jc-center body-box">
        <dv-scroll-board :config="config" style="width:100%;height:360px" />
      </div>
      <div class="ranking">
        <span style="color:#5cd9e8">
          <icon name="align-left"></icon>
        </span>
        <span class="fs-xl text mx-2 mb-1">的士行程汇报</span>
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
        ["ding", "da", "sd"],
        ["ding", "da", "sd"],
        ["ding", "da", "sd"],
        ["ding", "da", "sd"]
      ],
      ranking: {
        data: [],
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
      for(var idx = 0; idx<tmp.length; idx++){
        var taxiId = tmp[idx]['name'].replace('的士编号：','');
        if(tmp[idx]['guest'].length==1){
          order_to_taxi.push([tmp[idx]['guest'][0],taxiId,"<span  class='colorRed'>独享</span>"]);
        }
        else{
          for(let index = 0; index < tmp[idx]['guest'].length ; index++)
            order_to_taxi.push([tmp[idx]['guest'][index],taxiId,"<span  class='colorGrass'>拼车</span>"]);
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
</style>