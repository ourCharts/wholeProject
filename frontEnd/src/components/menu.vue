<template>
  <el-container>

    <el-row :gutter="20">
      <el-col><el-input v-model="input1" placeholder="请输入内容"></el-input></el-col>
      <el-col><el-input v-model="input2" placeholder="请输入内容"></el-input></el-col>
      <el-col><el-button type="primary" v-on:click="hello" id="king">主要按钮</el-button></el-col>
    </el-row>
    <el-row :gutter="20">

      <el-input v-model="input3" placeholder="Order_id"></el-input>
      <el-button type="primary" v-on:click="getsth">拿东西</el-button>
    </el-row>
  </el-container>

</template>

<script>

export default {
  name: 'amenu',
  data () {
    return {
      input1: 120,
      input2: 30,
      input3: '39a096b71376b82f35732eff6d95779b'
    }
  },
  methods: {
    hello: function () {
      this.$emit('added', this.input1, this.input2)
    },
    debugg: function () {
      console.log('debugging')
    },
    getsth: function () {
      this.$emit('order', this.input3)
    }
  }

}
</script>

<style>
</style>
