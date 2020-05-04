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
      config: {
        header: ["订单编号", "对应的士", "完成情况"],
        data: [
          ["组件1", "dev-1", "<span  class='colorGrass'>↑75%</span>"],
          ["组件2", "dev-2", "<span  class='colorRed'>↓33%</span>"],
          ["组件3", "dev-3", "<span  class='colorGrass'>↑100%</span>"],
          ["组件4", "rea-1", "<span  class='colorGrass'>↑94%</span>"],
          ["组件5", "rea-2", "<span  class='colorGrass'>↑95%</span>"],
          ["组件6", "fix-2", "<span  class='colorGrass'>↑63%</span>"],
          ["组件7", "fix-4", "<span  class='colorGrass'>↑84%</span>"],
          ["组件8", "fix-7", "<span  class='colorRed'>↓46%</span>"],
          ["组件9", "dev-2", "<span  class='colorRed'>↓13%</span>"],
          ["组件10", "dev-9", "<span  class='colorGrass'>↑76%</span>"]
        ],
        rowNum: 7, //表格行数
        headerHeight: 40,
        headerBGC: "#0f1325", //表头
        oddRowBGC: "#0f1325", //奇数行
        evenRowBGC: "#171c33", //偶数行
        index: true,
        columnWidth: [50],
        align: ["center"]
      },
      ranking: {
        data: [
          {
            name: "周口",
            value: 55
          },
          {
            name: "南阳",
            value: 100
          },
          {
            name: "西峡",
            value: 78
          },
          {
            name: "驻马店",
            value: 66
          },
          {
            name: "新乡",
            value: 80
          },
          {
            name: "新乡",
            value: 80
          },
          {
            name: "新乡",
            value: 80
          },
          {
            name: "新乡",
            value: 80
          }
        ],
        waitTime: 4000,
        unit: "%",
      },
    };
  },
  components: {},
  mounted() {},
  methods: {}
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