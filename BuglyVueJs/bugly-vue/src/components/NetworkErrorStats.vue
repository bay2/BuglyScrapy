<template>
  <ve-bar :data="chartData" :settings="chartSettings" :grid="grid"></ve-bar>
</template>

<script>
  import axios from 'axios'
  export default {
    data () {
      this.grid = {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      this.chartSettings = {
        metrics: ['count'],
        legendName: {
          'count': '接口超时次数'
        }
        
      }
      return {
        chartData: {
          columns: ['name', 'count'],
          rows: []
        },
        errorData: null
      }
    },
    mounted () {
      // eslint-disable-next-line
      console.log(process.env.VUE_APP_ROOT_API)
      axios
      // eslint-disable-next-line
      .get(process.env.VUE_APP_ROOT_API + '/networkErrorSum', {params: {count: 10}})
      .then(response => (this.chartData.rows = response.data['data']))
    }
  }
</script>