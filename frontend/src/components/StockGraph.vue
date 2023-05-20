<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div ref="chartContainer" class="stock-graph">
    <div class="tooltipDate" ref="tooltipDate"></div>
    <div class="tooltip" ref="tooltip"></div>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import { defineComponent, onMounted, PropType, ref } from 'vue'
import { getStocksData, getPerformancesData } from '../services/apiService'

export default defineComponent({
  name: 'StockGraph',
  props: {
    width: {
      type: Number,
      default: 800
    },
    height: {
      type: Number,
      default: 400
    },
    margin: {
      type: Object as PropType<{
        top: number;
        right: number;
        bottom: number;
        left: number;
      }>,
      default: () => ({ top: 20, right: 20, bottom: 30, left: 50 })
    },
    colors: {
      type: Array as PropType<string[]>,
      default: () => ['steelblue', 'green', 'red']
    }
  },
  setup (props) {
    const chartContainer = ref<HTMLDivElement | null>(null)
    const tooltip = ref<HTMLDivElement | null>(null)
    const tooltipDate = ref<HTMLDivElement | null>(null)

    onMounted(async () => {
      const stocksData: { [key: string]: { date: string; value: number; price: number }[] } = await getStocksData()
      console.log('🚀 ~ file: StockGraph.vue:50 ~ onMounted ~ stocksData:', stocksData)
      const performancesData = await getPerformancesData()
      console.log('🚀 ~ file: StockGraph.vue:52 ~ onMounted ~ performancesData:', performancesData)

      if (chartContainer.value) {
        const { width, height, margin, colors } = props

        const lineDataKeys = Object.keys(stocksData)

        const validData = lineDataKeys.map((key) =>
          stocksData[key].map((d: { date: string; value: number, price: number }) => ({
            date: new Date(d.date),
            value: d.value
          }))
        )

        const x = d3
          .scaleTime()
          .domain([
            d3.min(validData, (lineData) => d3.min(lineData, (d) => d.date)) as Date,
            d3.max(validData, (lineData) => d3.max(lineData, (d) => d.date)) as Date
          ])
          .range([margin.left, width - margin.right])

        const y = d3
          .scaleLinear()
          .domain([
            0,
            d3.max(validData, (lineData) => d3.max(lineData, (d) => d.value)) as number
          ])
          .nice()
          .range([height - margin.bottom, margin.top])

        const line = d3
          .line<{ date: Date; value: number }>()
          .defined((d) => !isNaN(d.value))
          .x((d) => x(new Date(d.date)))
          .y((d) => y(d.value))

        const svg = d3.select(chartContainer.value).append('svg')
          .attr('width', width)
          .attr('height', height)

        validData.forEach((lineData, i) => {
          svg
            .append('path')
            .datum(lineData)
            .attr('class', 'line')
            .attr('fill', 'none')
            .attr('stroke', colors[i % colors.length])
            .attr('stroke-width', 2)
            .attr('d', line)
        })

        svg
          .append('g')
          .attr('transform', `translate(0,${height - margin.bottom})`)
          .call(d3.axisBottom(x))

        svg
          .append('g')
          .attr('transform', `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))

        // Crosshair lines
        const focus = svg.append('g')
          .style('display', 'none')

        focus.append('line')
          .attr('class', 'focus-line-x')
          .attr('stroke', 'gray')
          .attr('stroke-dasharray', '3,3')
          .attr('y1', margin.top)
          .attr('y2', height - margin.bottom)

        focus.append('line')
          .attr('class', 'focus-line-y')
          .attr('stroke', 'gray')
          .attr('stroke-dasharray', '3,3')
          .attr('x1', margin.left)
          .attr('x2', width - margin.right)

        const overlay = svg.append('rect')
          .attr('class', 'overlay')
          .attr('width', width - margin.left - margin.right)
          .attr('height', height - margin.top - margin.bottom)
          .style('fill', 'none')
          .style('pointer-events', 'all')

        overlay.on('mouseover', () => focus.style('display', null))
          .on('mouseout', () => focus.style('display', 'none'))
          .on('mousemove', mousemove)

        function mousemove (event: MouseEvent) {
          const [xMouse, yMouse] = d3.pointer(event)
          const bisectDate = d3.bisector((d: { date: Date }) => d.date).left

          lineDataKeys.forEach((lineKey) => {
            const lineData = stocksData[lineKey]
            const bisectIndex = bisectDate(
              lineData.map((d) => ({ date: new Date(d.date), value: d.value, price: d.price })),
              x.invert(xMouse)
            )
            const d = lineData[bisectIndex]

            const xPos = x(new Date(d.date))
            const yPos = y(y.invert(yMouse))

            focus.select('.focus-line-x')
              .attr('x1', xPos)
              .attr('x2', xPos)

            focus.select('.focus-line-y')
              .attr('y1', yPos)
              .attr('y2', yPos)

            // Access the tooltip element
            const tooltipValue = tooltip.value as HTMLDivElement
            const tooltipDateValue = tooltipDate.value as HTMLDivElement

            if (tooltipValue) {
              let tooltipContent = ''

              lineDataKeys.forEach((lineKey) => {
                const lineData = stocksData[lineKey]
                const bisectIndex = bisectDate(
                  lineData.map((d) => ({ date: new Date(d.date), value: d.value, price: d.price })),
                  x.invert(xMouse)
                )
                const d = lineData[bisectIndex]
                tooltipContent += `${lineKey}: ${d.value}, ${d.price.toFixed(2)}<br>`
              })
              tooltipValue.style.display = 'block'
              tooltipValue.innerHTML = tooltipContent

              if (tooltipDateValue) {
                tooltipDateValue.style.display = 'block'
                tooltipDateValue.innerHTML = `${d.date}`
              }
            }
          })
        }
      }
    })

    return { chartContainer, tooltip, tooltipDate }
  }
})
</script>

<style scoped>
.stock-graph {
  font-family: Arial, sans-serif;
}

.tooltip,
.tooltipDate {
  pointer-events: none;
  background-color: white;
  padding: 4px;
}

.focus-line-x,
.focus-line-y {
  fill: none;
  stroke: gray;
  stroke-dasharray: 3, 3;
}
</style>
