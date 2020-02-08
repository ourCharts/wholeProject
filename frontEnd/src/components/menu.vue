<template>
  <el-container>

    <el-input v-model="input1" placeholder="请输入内容"></el-input>
    <el-input v-model="input2" placeholder="请输入内容"></el-input>
    <el-button type="primary" v-on:click="hello" id="king">主要按钮</el-button>
    <el-button type="primary" v-on:click="getsth">拿东西</el-button>
  </el-container>

</template>

<script>
import $ from 'jquery'
export default {
  name: 'amenu',
  data () {
    return {
      input1: 120,
      input2: 30
    }
  },
  methods: {
    hello: function () {
      this.$emit('added', this.input1, this.input2)
    },
    getsth: function () {
      $.get('http://127.0.0.1:8000/initial_status/',
        {
          order_id: 13
        },
        function (data) {
          alert(data)
        })
    }
  }
}
</script>

<style>
</style>
