<template>
  <div id="center">
    <div class="up">
      <div class="item bg-color-black" v-for="item in titleItem" :key="item.title">
        <dv-border-box-8>
          <p class="colorBlue fw-b" style="line-height: 30px; font-size:1.5rem">{{item.title}}</p>
          <div>

            <p class="conuts" style="width:100px;height:50px;">{{item.number}}</p>
          </div>
        </dv-border-box-8>
      </div>
    </div>
    <div class="down">
      <div class="percent">
        <div class="item  bg-color-black">
          <span>今日任务通过率</span>
          <centerChart1 />
        </div>
        <div class="item  bg-color-black">
          <span>今日任务达标率</span>
          <centerChart2 />
        </div>
      </div>
    </div>
    <!-- <div class="down">
      <dv-border-box-11 title="hello" :color="['#1A5CD7', '#257dff']">
        <div class="item">
          
          <dv-active-ring-chart :config="config" style="width:300px;height:300px" />
        </div>
      </dv-border-box-11 >
      <dv-border-box-11 title="hello">
        <div class="item">
          
          <dv-active-ring-chart :config="config" style="width:300px;height:300px" />
        </div>
      </dv-border-box-11>
    </div> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      titleItem: [
        {
          title: "今日订单数",
          number: 120
        },
        {
          title: "已完成订单数",
          number: 7
        },
        {
          title: "处理订单数",
          number: 9
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
      ],
      config: {
        digitalFlopStyle: {
          fontSize: 30,

          fill: "#fff"
        },
        lineWidth: 10,
        data: [
          {
            name: "周口",
            value: 55
          },
          {
            name: "南阳",
            value: 120
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
          }
        ]
      }
    };
  },
  mounted() {
    setInterval(() => {
      var tmp = document.getElementsByClassName("active-ring-name")[0];
      tmp.style.lineHeight = "30px";
    }, 300);
  }
};
</script>

<style lang="scss" scoped>
.conuts {
    color: #00fbfe;
    text-shadow: 0 0 25px #00fbfe;
    font-size: 28px;
    font-weight: bolder;
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
    justify-content: space-between;
    .bg-color-black {
      border-radius: 5px;
    }
    .ranking {
      padding: 10px;
      width: 59%;
    }
    .percent {
      width: 40%;
      display: flex;
      flex-wrap: wrap;
      .item {
        width: 50%;
        height: 200px;
        span {
          margin-top: 7px;
          display: flex;
          justify-content: center;
        }
      }
    }
  }
}
</style>