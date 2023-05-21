<template>
  <div id="app">
    <div class="title">Stock market prices</div>
    <div class="stock-graph-container">
      <StockGraph />
    </div>
    <div class="stock-table-container">
      <StockTable />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import StockGraph from './components/StockGraph.vue'
import StockTable from './components/StockTable.vue'

export default defineComponent({
  name: 'App',
  components: {
    StockGraph,
    StockTable
  }
})
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.title {
  padding: 3%;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 40px;
  color: #131722;
}

.stock-graph-container,
.stock-table-container {
  width: 100%;
  margin: 10px;
}
</style>
