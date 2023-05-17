<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div ref="chartContainer" class="stock-graph">
    <div class="tooltip" ref="tooltip"></div>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'

import { defineComponent, onMounted, PropType, ref } from 'vue'

export default defineComponent({
  name: 'StockGraph',
  props: {
    data: {
      type: Object as PropType<{ [key: string]: { date: string; value: number }[] }>,
      required: true
    },
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

    onMounted(() => {
      if (chartContainer.value) {
        const { width, height, margin, data, colors } = props

        const lineDataKeys = Object.keys(data)

        const validData = lineDataKeys.map((key) =>
          data[key].map((d: { date: string; value: number }) => ({
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
          // console.log('🚀 ~ file: StockGraph.vue:137 ~ mousemove ~  [xMouse, yMouse] :', [xMouse, yMouse])
          const bisectDate = d3.bisector((d: { date: Date }) => d.date).left

          lineDataKeys.forEach((lineKey) => {
            const lineData = data[lineKey]
            // console.log('🚀 ~ file: StockGraph.vue:142 ~ lineDataKeys.forEach ~ lineData:', lineData)
            const bisectIndex = bisectDate(
              lineData.map((d) => ({ date: new Date(d.date), value: d.value })), // Convert date strings to Date objects
              x.invert(xMouse)
            )
            const d = lineData[bisectIndex]
            const xPos = x(new Date(d.date))
            const yPos = y(d.value)

            focus.select('.focus-line-x')
              .attr('x1', xPos)
              .attr('x2', xPos)

            focus.select('.focus-line-y')
              .attr('y1', yPos)
              .attr('y2', yPos)

            const tooltipValue = tooltip.value ? (tooltip.value as unknown as Record<string, HTMLDivElement>)[lineKey] : null
            console.log('🚀 ~ file: StockGraph.vue:159 ~ lineDataKeys.forEach ~ tooltipValue:', tooltipValue, tooltip)
            if (tooltipValue) {
              tooltipValue.style.display = 'block'
              tooltipValue.style.left = `${xPos}px`
              tooltipValue.style.top = `${yPos - 20}px`
              tooltipValue.textContent = `Value: ${d.value}`
            }
          })
        }
      }
    })

    return { chartContainer, tooltip }
  }
})
</script>

<style scoped>
.stock-graph {
  font-family: Arial, sans-serif;
}

.tooltip {
  position: absolute;
  pointer-events: none;
  background-color: white;
  border: 1px solid gray;
  padding: 4px;
}

.focus-line-x,
.focus-line-y {
  fill: none;
  stroke: gray;
  stroke-dasharray: 3, 3;
}
</style>
