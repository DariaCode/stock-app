<template>
  <div class="performance-table-container">
    <table class="performance-table">
      <thead>
        <tr>
          <th>Stock</th>
          <th>Open</th>
          <th>High</th>
          <th>Low</th>
          <th>Close</th>
          <th>Volume</th>
          <th>Annualized Return</th>
          <th>Annualized Volatility</th>
          <th>Cumulative Return</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(performance, stock) in performancesData" :key="stock">
          <td>{{ stock }}</td>
          <td>{{ Math.round(performance.open) }}</td>
          <td>{{ Math.round(performance.high) }}</td>
          <td>{{ Math.round(performance.low) }}</td>
          <td>{{ Math.round(performance.close) }}</td>
          <td>{{ Math.round(performance.volume) }}</td>
          <td>{{ Math.round(performance.annualized_return) }}%</td>
          <td>{{ Math.round(performance.annualized_volatility) }}%</td>
          <td>{{ Math.round(performance.cumulative_return) }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { getPerformancesData } from '../services/apiService'
import { PerformanceData } from './Models'

export default defineComponent({
  name: 'PerformanceTable',
  setup () {
    const performancesData = ref<Record<string, PerformanceData>>({})

    onMounted(async () => {
      try {
        performancesData.value = await getPerformancesData()
      } catch (error) {
        console.error('Error fetching performances data:', error)
      }
    })

    return { performancesData }
  }
})
</script>

<style scoped>
.performance-table-container {
  display: flex;
  justify-content: center;
}

.performance-table {
  width: 80%;
  border-collapse: collapse;
  text-align: center;
  color: #131722;
  font-family: Arial, Helvetica, sans-serif;
}

.performance-table th,
.performance-table td {
  padding: 8px;
  border: 1px solid #daf2ee;
}

.performance-table th {
  background-color: #daf2ee;
}
</style>
