<template>
  <div id="center">
    <div class="up">
      <div class="item bg-color-black" v-for="item in titleItem" :key="item.title">
        <dv-border-box-8 >
          <p class="colorBlue fw-b" style="line-height: 30px; font-size:1.5rem">{{item.title}}</p>
          <div>

            <p class="conuts">{{item.number}}</p>
          </div>
        </dv-border-box-8>
      </div>
    </div>
    <div class="down">
        <div class="colorBlue item fw-b" style="line-height: 30px; font-size:1.5rem">
          <span>今日订单组成</span>
          <centerChart1 />
        </div>
    </div>
  </div>
</template>

<script>
import centerChart1 from "@/components/echart/center/centerChart1";

export default {
  components:{
    centerChart1
  },
  data() {
    return {
      order_finished:[],
      order_got:0,
      order_fail:0
    };
  },
  computed:{
    titleItem: function () {
      return [
        {
          title: "今日订单数",
          number: this.order_got
        },
        {
          title: "已完成订单数",
          number: this.order_finished.length
        },
        {
          title: "处理订单数",
          number: this.order_got - this.order_fail
        },
        {
          title: "拼车订单数",
          number: 12
        },
        {
          title: "在线出租车",
          number: 23
        },
        {
          title: "空闲出租车",
          number: 24
        }
      ]
    }
  },
  mounted(){
      this.$bus.$on('order_finished',(data) =>{
          this.order_finished=data[0],
          this.order_got=data[1],
          this.order_fail=data[2]
      });

  }
};
</script>

<style lang="scss" scoped>
.conuts {
    color: #00fbfe;
    text-shadow: 0 0 25px #00fbfe;
    font-size: 28px;
    font-weight: bolder;
    text-align: center;
    width:100px;
    margin: auto;
    height:50px;
    line-height: 30px;
}
#center {
  display: flex;
  flex-direction: column;
  .up {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    .item {
      border-radius: 5px;
      padding-top: 1rem;
      margin-top: 0.5rem;
      width: 50%;
      height: 20%;
    }
  }
  .down {
    padding: 4px;
    padding-bottom: 0px;
    width: 100%;
    display: flex;
    height: 255px;
    justify-content: space-around;
  }
}
</style>