<template>
  <div id="index">
    <!-- <dv- full-screen-container style="position:initial"> -->
    <!-- <dv-loading v-if="loading">Loading...</dv-loading> -->
    <div  class="host-body">
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
            <span class="text">2020年03月16日 周一 12:00</span>
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
              <center/>
            </dv-border-box-10>
          </div>
          <dv-decoration-2 :reverse="true" style="width:10px;height:500px;"  />
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="bottomLeft">
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
        <!-- 第四行数据 -->
        <div class="bototm-box">
          <dv-border-box-13>
            <bottomLeft />
          </dv-border-box-13>
          <dv-border-box-12>
            <bottomRight />
          </dv-border-box-12>
        </div>
      </div>
    </div>
    <!-- </dv-full-screen-container> -->
  </div>
</template>

<script>
import centreLeft1 from "./display/centreLeft1";
import centreLeft2 from "./display/centreLeft2";
import centreRight1 from "./display/centreRight1";
import centreRight2 from "./display/centreRight2";
import center from "./display/center";
import bottomLeft from "./display/bottomLeft";
import bottomRight from "./display/bottomRight";
import Map from "./map";
export default {
  name: "index",
  data() {
    return {
      loading: true
    };
  },
  components: {
    Map,
    bottomLeft,
    centreLeft1,
    centreLeft2,
    centreRight1,
    centreRight2,
    center,
    bottomRight
  },
  mounted() {
    this.cancelLoading();
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
#bottomLeft {
  padding: 1.5rem 1rem;
  height: 750px;
  min-width: 300px;
  border-radius: 5px;
  .text {
    color: #c3cbde;
  }
  .chart-box {
    margin-top: 1rem;
    width: 170px;
    height: 1200px;
    .active-ring-name {
      padding-top: 10px;
    }
  }
}
@import "../assets/scss/index.scss";
</style>
