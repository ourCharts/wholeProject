<template>
  <div>
    <i class="el-icon-edit-outline" id="diy"></i>
    <el-row type="flex">
      <el-input v-model="input1" ></el-input>
      <el-input v-model="input2" ></el-input>
      <el-button type="warning" v-on:click="hello" id="king">自定义添加点</el-button>
    </el-row>
    <el-row type="flex">
      <el-button type="warning" v-on:click="addThree">添加3个order</el-button>
    </el-row>
    <el-row type="flex">
      <el-input v-model="input3" placeholder="Order_id"></el-input>
      <el-button type="warning" v-on:click="getsth">添加订单路径</el-button>
    </el-row>
    <i class="el-icon-document" id="diy"></i>
    <el-row>
      <el-card class="box-card" shadow="hover" v-for="x in arr" :key="x">
          {{x}}
      </el-card>
    </el-row>
  </div>

</template>

<script>
import $ from 'jquery'
export default {
  name: 'amenu',
  data () {
    return {
      input1: 120,
      input2: 30,
      input3: '39a096b71376b82f35732eff6d95779b',
      arr: []
    }
  },
  methods: {
    sleep: function (ms) {
      return new Promise(function (resolve, reject) {
        setTimeout(resolve, ms)
      })
    },
    hello: function () {
      this.$emit('added', this.input1, this.input2)
    },
    addThree: function () {
      var _this = this
      for (let i = 0; i < 6; i++) {
        this.sleep(i * 100).then(function () {
          console.log(i + '---->' + _this.arr[i])
          _this.$emit('order', _this.arr[i])
        })
      }
    },
    debugg: function () {
      console.log('debugging')
    },
    getsth: function () {
      this.$emit('order', this.input3)
    },
    init: function () {
      var _this = this
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/all_id/',
        async: true,
        success: function (response) {
          var obj = response
          for (let i = 0; i < 10; i++) {
            _this.arr.push(obj[i].order_id)
          }
        }
      })
    }
  },
  mounted () {
    this.init()
  }
}
</script>

<style>
  #diy{
    color: #9e7d60ff;
    font-size: 200%;
    margin-bottom: 20px
  }
  .el-row{
    margin-bottom: 10px
  }
  .el-card{
    margin-bottom: 10px;
    background-color: #2F4050;
    color: #9e7d60ff;
    border-color: #9e7d60ff;
    font-size: 10px;
  }
  .el-card__body{
    padding: 3px !important
  }
   .el-input__inner{
    background-color: #3F444C !important;
    color: #9e7d60ff;
    border-color: #9e7d60ff
  }
  .el-input__inner:focus{
    border-color: white !important
  }
  .el-button{
    padding: 5px !important
  }
  .el-button,.el-button:focus{
    background-color: #2F4050 !important;
    color: #9e7d60ff !important;
    border-color: #9e7d60ff !important
  }
  .el-button:hover{
    background-color: #3F444C !important;
    color: #9e7d60ff;
    border-color: #9e7d60ff
  }
</style>
