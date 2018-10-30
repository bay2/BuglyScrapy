<template>
    <ve-line :data="chartData" :settings="chartSettings" :title="titleSettings"></ve-line>
</template>

<script>
import axios from 'axios'
export default {
    data () {
    this.titleSettings = {
        text: '今日接口超时次数',
        top: '0',
        left: '0'
    },
    this.chartSettings = {
        metrics: ['count'],
        legendName: {
            'count': '接口超时次数'
        },
        labelMap: {
          'count': '接口超时次数',
          'hour': '小时'
        },
        dimension: ['hour']
    }
    return {
        chartData: {
          columns: ['hour', 'count'],
          rows: [
          ]
        }
      }
    },
    mounted () {
      axios
      .get('http://localhost:5000/daytimestats')
      .then(response => (this.chartData.rows = response.data['data']))
    }
}
</script>

