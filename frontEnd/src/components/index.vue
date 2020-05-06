<template>
  <div id="index">
    <!-- <dv- full-screen-container style="position:initial"> -->
    <!-- <dv-loading v-if="loading">Loading...</dv-loading> -->
    <div class="host-body">
      <div class="d-flex jc-center">
        <dv-decoration-10 style="width:33.3%;height:5px;" />
        <div class="d-flex jc-center">
          <dv-decoration-8 :color="['#568aea', '#000000']" style="width:200px;height:50px;" />
          <div class="title">
            <span class="title-text">大数据可视化平台</span>
            <dv-decoration-5
              class="title-bototm"
              :reverse="true"
              :color="['#50e3c2', '#67a1e5']"
              style="width:250px;height:40px;padding-top:30px"
            />
          </div>
          <dv-decoration-8
            :reverse="true"
            :color="['#568aea', '#000000']"
            style="width:200px;height:50px;"
          />
        </div>
        <dv-decoration-10 style="width:33.3%;height:5px;" />
      </div>

      <!-- 第二行 -->
      <div class="d-flex jc-between px-2">
        <div style="width: 40%" class="d-flex">
          <div
            class="react-left mr-4"
            style="width: 500px; background-color: #0f1325; text-align: right;"
          >
            <span class="react-after"></span>
            <span class="text">{{realTime}}</span>
          </div>
        </div>
      </div>

      <div class="body-box">
        <!-- 第三行数据 -->
        <div class="content-box">
          <div style="flex-shrink:7; width:2000px">
            <dv-border-box-10 style="flex-shrink:7;">
              <div class="d-flex pt-2 pl-2">
                <span>
                  <icon name="chart-bar" id="icon-map"></icon>
                </span>
                <div class="d-flex">
                  <span class="fs-xl text mx-2">总体信息</span>
                </div>
              </div>
              <center />
            </dv-border-box-10>
          </div>
          <dv-decoration-2 :reverse="true" style="width:10px;height:500px;" />
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="first_line">
              <div class="d-flex pt-2 pl-2">
                <span>
                  <icon name="chart-bar" id="icon-map"></icon>
                </span>
                <div class="d-flex">
                  <span class="fs-xl text mx-2">实时路径地图</span>
                </div>
              </div>
              <Map />
            </dv-border-box-13>
          </div>
          <dv-decoration-2 :reverse="true" style="width:5px;height:500px;" />
          <div style="flex-shrink:7; width:2000px">
            <dv-border-box-13 style="flex-shrink:7;">
              <centreRight1 />
            </dv-border-box-13>
          </div>
        </div>

        <dv-decoration-10 style="width:100%;height:5px;padding-top:5px;padding-bottom:5px" />
        <!-- 热力图、订单的士比、碳排放量 -->
        <div class="bototm-box">
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="second_line">
              <div class="d-flex pt-2 pl-2">
                <span>
                  <icon name="chart-bar" id="icon-map"></icon>
                </span>
                <div class="d-flex">
                  <span class="fs-xl text mx-2">实时路径地图</span>
                </div>
              </div>
              <Heat />
            </dv-border-box-13>
          </div>
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="second_line">
              <div class="d-flex pt-2 pl-2">
                <span>
                  <icon name="chart-bar" id="icon-map"></icon>
                </span>
                <div class="d-flex">
                  <span class="fs-xl text mx-2">订单的士比</span>
                </div>
              </div>
              <bottomLeftChart/>
            </dv-border-box-13>
          </div>
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="second_line">
              <div class="d-flex pt-2 pl-2">
                <span>
                  <icon name="chart-bar" id="icon-map"></icon>
                </span>
                <div class="d-flex">
                  <span class="fs-xl text mx-2">碳排放量</span>
                </div>
              </div>
              <bottomRightChart />
            </dv-border-box-13>
          </div>
        </div>
      </div>
    </div>
    <!-- </dv-full-screen-container> -->
  </div>
</template>

<script>
import centreRight1 from "./display/centreRight1";
import center from "./display/center";
import bottomLeftChart from '@/components/echart/bottom/bottomLeftChart';
import bottomRightChart from "./echart/bottom/bottomRightChart"
import Map from "./map";
import Heat from "./heat";
export default {
  name: "index",
  data() {
    return {
      loading: true,
      realTime: '2016年11月01日 周二 12:00'
    };
  },
  components: {
    Map,
    bottomRightChart,
    bottomLeftChart,
    Heat,
    centreRight1,
    center,
  },
  mounted() {
    this.$bus.on('realTime', (val)=>{
      this.realTime = val
    })
    this.cancelLoading();
  },
  beforeDestroy() {
    this.$bus.off('realTime')
  },
  methods: {
    cancelLoading() {
      setTimeout(() => {
        this.loading = false;
      }, 2000);
    }
  }
};
</script>

<style lang="scss" scoped>
#icon-map {
  color: #5cd9e8 !important;
}
#first_line {
  padding: 1.5rem 1rem;
  height: 750px;
  min-width: 300px;
  border-radius: 5px;
  .text {
    color: #c3cbde;
  }
}
#second_line{
  padding: 1.5rem 1rem;
  height: 400px;
  min-width: 300px;
  border-radius: 5px;
}
@import "../assets/scss/index.scss";
</style>
