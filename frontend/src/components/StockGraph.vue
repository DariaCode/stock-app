<!-- eslint-disable @typescript-eslint/no-explicit-any -->
<template>
  <div ref="chartContainer" class="stock-graph">
    <div ref="chartContainer" class="chart-container">
      <div class="tooltips">
        <div class="tooltipDate" ref="tooltipDate"></div>
        <div class="tooltip" ref="tooltip"></div>
        <div ref="legendContainer" class="legend-container"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import * as d3 from 'd3'
import { defineComponent, onMounted, PropType, ref } from 'vue'
import { getStocksData } from '../services/apiService'
import { Stock } from './Models'

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
      default: () => ['#00bcd4', '#089981', '#d81b60']
    }
  },
  setup (props) {
    const chartContainer = ref<HTMLDivElement | null>(null)
    const legendContainer = ref<HTMLDivElement | null>(null)
    const tooltip = ref<HTMLDivElement | null>(null)
    const tooltipDate = ref<HTMLDivElement | null>(null)
    const stocksData = ref<Record<string, Stock[]>>({})

    const fetchStocksData = async () => {
      try {
        stocksData.value = await getStocksData()
      } catch (error) {
        console.error('Error fetching stocks data:', error)
      }
    }

    onMounted(async () => {
      await fetchStocksData()
      updateChart()
    })

    // Fetch data every 10 minutes
    setInterval(fetchStocksData, 600000)

    const updateChart = () => {
      if (chartContainer.value) {
        const { width, height, margin, colors } = props

        const lineDataKeys = Object.keys(stocksData.value)

        const validData = lineDataKeys.map((key) =>
          stocksData.value[key].map((d: Stock) => ({
            date: new Date(d.date),
            value: d.value,
            price: d.price
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
            const lineData = stocksData.value[lineKey]
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

            // Tooltip elements
            const tooltipValue = tooltip.value as HTMLDivElement
            const tooltipDateValue = tooltipDate.value as HTMLDivElement

            if (tooltipDateValue) {
              tooltipDateValue.style.display = 'block'
              tooltipDateValue.innerHTML = `${new Date(d.date).toDateString()}`
            }

            if (tooltipValue) {
              let tooltipContent = `<table style="width:270px">
                  <tr>
                    <th style="width:90px">Stock</th>
                    <th style="width:90px">Value</th>
                    <th style="width:90px">Price</th>
                  </tr>`

              lineDataKeys.forEach((lineKey) => {
                const lineData = stocksData.value[lineKey]
                const bisectIndex = bisectDate(
                  lineData.map((d) => ({ date: new Date(d.date), value: d.value, price: d.price })),
                  x.invert(xMouse)
                )
                const d = lineData[bisectIndex]
                tooltipContent += `<tr><th>${lineKey}</th><th>${d.value}</th><th>${d.price.toFixed(2)}</th></tr>`
              })
              tooltipValue.style.display = 'flex'
              tooltipValue.innerHTML = tooltipContent + '</table>'
            }
          })
        }

        // Legend
        const legendColors = colors.slice(0, lineDataKeys.length)
        const legendLabels = lineDataKeys

        const legendContainerValue = legendContainer.value as HTMLDivElement

        const legend = d3.select(legendContainerValue).append('svg')
          .attr('width', width)
          .attr('height', 50)

        legend.selectAll('rect')
          .data(legendColors)
          .enter()
          .append('rect')
          .attr('x', (d, i) => i * 100)
          .attr('y', 10)
          .attr('width', 20)
          .attr('height', 20)
          .attr('fill', (d) => d)

        legend.selectAll('text')
          .data(legendLabels)
          .enter()
          .append('text')
          .attr('x', (d, i) => i * 100 + 30)
          .attr('y', 25)
          .text((d) => d)
          .style('font-size', '14px')
          .style('fill', 'black')
      }
    }

    return { chartContainer, legendContainer, tooltip, tooltipDate }
  }
})
</script>

<style scoped>
.stock-graph {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: Arial, sans-serif;
  flex-direction: row-reverse;
}

.legend-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  max-width: 280px;
  min-height: 280px;
}

.chart-container {
  position: relative;
}

.tooltipDate {
  color: #089981;
  font-weight: 800;
  font-size: 18px;
}

.tooltips {
  font-family: Arial, Helvetica, sans-serif;
  text-align: center;
  color: #131722;
}

.tooltip,
.tooltipDate {
  pointer-events: none;
  padding: 4px;
  justify-content: space-around;
}

.focus-line-x,
.focus-line-y {
  fill: none;
  stroke: gray;
  stroke-dasharray: 3, 3;
}
</style>
