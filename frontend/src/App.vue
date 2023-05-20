<template>
  <div id="app">
    <StockGraph />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import StockGraph from './components/StockGraph.vue'

export default defineComponent({
  name: 'App',
  components: {
    StockGraph
  }
})
</script>

<style>
#app {
  text-align: center;
  padding: 20px;
}
</style>
