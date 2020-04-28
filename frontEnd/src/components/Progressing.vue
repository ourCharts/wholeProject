<template>
  <el-container>
    <div class="progress"
        style="width: 100%">
      <div
        class="progress-bar"
        role="progressbar"
        
        aria-valuenow="50"
        aria-valuemin="0"
        aria-valuemax="100"
      ></div>;
    </div>
  </el-container>
</template>
<script>
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
export default {
  name: "Progressing",
  props: ['progess_s'],
  data() {
    return {
        progess_s: this.progess_s
    };
  }
};
</script>