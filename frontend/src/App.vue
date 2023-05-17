<template>
  <div id="app">
    <StockGraph :data="stockData" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import StockGraph from './components/StockGraph.vue'
import stockData from './services/mock-response'

export default defineComponent({
  name: 'App',
  components: {
    StockGraph
  },
  data () {
    return {
      stockData: stockData
    }
  }
})
</script>

<style>
#app {
  text-align: center;
  padding: 20px;
}
</style>
