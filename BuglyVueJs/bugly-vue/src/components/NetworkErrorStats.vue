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
      axios
      .get('http://localhost:5000/networkErrorSum', {params: {count: 10}})
      .then(response => (this.chartData.rows = response.data['data']))
    }
  }
</script>