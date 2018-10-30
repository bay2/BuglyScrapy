<template>
  <div id="app">
    <div>
      <NetworkErrorStats/>
      <NetworkStatsDayTime style="margin-top: 60px;"/>
    </div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import NetworkErrorStats from './components/NetworkErrorStats.vue'
import NetworkStatsDayTime from './components/NetworkStatsDayTime.vue'

export default {
  name: 'app',
  components: {
    HelloWorld,
    NetworkErrorStats,
    NetworkStatsDayTime
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
