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
        <div style="width: 49%" class="d-flex">
          <div
            class="react-left mr-4"
            style="width: 500px; background-color: 'rgba(0,0,0,0)'; text-align: right;"
          >
            <span class="text"></span>
          </div>
        </div>
        
      </div>

      <div class="body-box">
        <!-- 第三行数据 -->
        <div class="content-box">
          <div style="flex-shrink:7; width:2000px">
            <dv-border-box-10 style="flex-shrink:7;">
              <div class="d-flex pt-2 pl-2" style="text-align:center">
                <dv-decoration-11 class="king_subtitle">总体信息</dv-decoration-11>
              </div>
              <general />
            </dv-border-box-10>
          </div>
          <dv-decoration-2 :reverse="true" style="width:10px;height:500px;" />
          <div style="flex-shrink:2; width:2000px">
            <dv-border-box-13 id="first_line">
              <div class="d-flex pt-2 pl-2" style="text-align:center">
                <dv-decoration-11 class="king_subtitle">实时路径地图</dv-decoration-11>
                <!-- <span class="fs-xl text mx-2">实时路径地图</span> -->
              </div>
              <Map />
            </dv-border-box-13>
          </div>
          <dv-decoration-2 :reverse="true" style="width:5px;height:500px;" />
          <div style="flex-shrink:7; width:2000px">
            <dv-border-box-13 style="flex-shrink:7;">
              <orderAndTaxi />
            </dv-border-box-13>
          </div>
        </div>

        <dv-decoration-10 style="width:100%;height:5px;padding-top:5px;padding-bottom:5px" />
        <!-- 热力图、订单的士比、碳排放量 -->
        <div class="bototm-box">
          <div style="flex-shrink:7; width:3000px">
            <dv-border-box-13 id="second_line" style="flex-shrink:7;">
              <div class="d-flex pt-2 pl-2" style="text-align:center">
                <dv-decoration-11 class="king_subtitle">实时热力图</dv-decoration-11>
              </div>
              <Heat />
            </dv-border-box-13>
          </div>
          <div style="flex-shrink:2; width:3000px">
            <dv-border-box-13 id="second_line" style="flex-shrink:2;">
              <div class="d-flex pt-2 pl-2" style="text-align:center">
                <dv-decoration-11 class="king_subtitle">优化总结</dv-decoration-11>
              </div>
              <significance />
            </dv-border-box-13>
          </div>
          <div style="flex-shrink:7; width:3000px">
            <dv-border-box-13 id="second_line" style="flex-shrink:7;">
              <div class="d-flex pt-2 pl-2" style="text-align:center">
                <dv-decoration-11 class="king_subtitle">环保效应</dv-decoration-11>
              </div>
              <tree />
            </dv-border-box-13>
          </div>
        </div>
      </div>
    </div>
    <!-- </dv-full-screen-container> -->
  </div>
</template>

<script>
import orderAndTaxi from "./orderAndTaxi";
import general from "./general";
import significance from "./significance";
import tree from "./tree";
import Map from "./map";
import Heat from "./heat";
export default {
  name: "index",
  data() {
    return {
      loading: true
    };
  },
  components: {
    Map,
    general,
    tree,
    significance,
    Heat,
    orderAndTaxi
    // centreRight1,
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
.king_subtitle {
  width: 200px;
  height: 35px;
  margin: auto;
  margin-top: -10px;
  line-height: 20px;
  font-size: 1.6rem;
  letter-spacing: 3px;
}
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
#second_line {
  padding: 1.5rem 1rem;
  height: 500px;
  min-width: 300px;
  border-radius: 5px;
  justify-content: center;
  display: flex;
}
@import "../assets/scss/index.scss";
</style>
