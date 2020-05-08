<template>
  <div id="center">
    <div class="up">
      <div class="item bg-color-black" v-for="item in titleItem" :key="item.title">
        <dv-border-box-8>
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
import centerChart1 from "@/components/echart/centerChart1";

export default {
  name:'general',
  components: {
    centerChart1
  },
  data() {
    return {
      order_finished: [],
      order_got: 0,
      order_fail: 0,
      non_empty_taxi: 0,
      share_order: 0
    };
  },
  computed: {
    order_processed: function() {
      return this.order_got - this.order_fail;
    },
    empty_taxi: function() {
      return 100 - this.non_empty_taxi;
    },
    titleItem: function() {
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
          title: "受理订单数",
          number: this.order_processed
        },
        {
          title: "拼车订单数",
          number: this.share_order
        },
        {
          title: "在线出租车",
          number: 100
        },
        {
          title: "空闲出租车",
          number: this.empty_taxi
        }
      ];
    }
  },
  mounted() {
    this.$bus.on("order_finished", data => {
      this.order_finished = data[0];
      this.order_got = data[1];
      this.order_fail = data[2];
      this.non_empty_taxi = data[3];
      if (data[5] == "true") this.share_order += 2;
      this.$bus.emit("proportion", [
        this.order_got,
        this.order_fail,
        this.share_order,
        data[4]
      ]);
    });
    // this.$bus.on("type_of_share_true", data => {
    //     this.share_order += 2;
    // });
  },
  beforeDestroy() {
    this.$bus.off("order_finished");
    // this.$bus.off("type_of_share_true");
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
  width: 100px;
  margin: auto;
  height: 50px;
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