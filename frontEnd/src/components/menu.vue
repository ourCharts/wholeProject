<template>
    <div></div>

</template>

<script>
export default {
  name: 'amenu',
  data () {
    return {

    }
  },
  methods: {
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
    }
  },
  mounted () {
    this.init()
  }
}
</script>

<style>
</style>
