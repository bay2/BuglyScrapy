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
        metrics: ['count', 'accessUser'],
        legendName: {
            'count': '接口超时次数',
            'accessUser': '联网用户数'
        },
        labelMap: {
          'count': '接口超时次数',
          'hour': '小时',
          'accessUser': '联网用户数'
        },
        dimension: ['hour']
    }
    return {
        chartData: {
          columns: ['hour', 'count', 'accessUser'],
          rows: [
          ]
        }
      }
    },
    mounted () {
      axios
      // eslint-disable-next-line
      .get(process.env.VUE_APP_ROOT_API + '/daytimestats')
      .then(response => (this.chartData.rows = response.data['data']))
    }
}
</script>

