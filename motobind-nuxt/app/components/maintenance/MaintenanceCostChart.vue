<template>
  <div class="maintenance-cost-chart">
    <ClientOnly>
      <div v-if="chartData && chartData.length > 0" class="chart-box">
        <apexchart
          ref="chartRef"
          type="area"
          height="220"
          width="100%"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>
      <div v-else class="no-data">
        <i class="fa-solid fa-chart-line"></i>
        <p>Нет данных о затратах</p>
      </div>

      <template #fallback>
        <div class="no-data">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <p>Загрузка графика...</p>
        </div>
      </template>
    </ClientOnly>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, nextTick } from 'vue'
import VueApexCharts from 'vue3-apexcharts'

// Используем defineAsyncComponent, чтобы точно избежать проблем с SSR
const apexchart = defineAsyncComponent(() => import('vue3-apexcharts'))

const props = defineProps({
  chartData: {
    type: Array,
    default: () => []
  }
})

const chartRef = ref(null)

// Принудительный ресайз после монтирования (лечит баг с 0px ширины)
onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      window.dispatchEvent(new Event('resize'))
    }, 200)
  })
})

const maxValue = computed(() => {
  if (!props.chartData.length) return 1000
  const max = Math.max(...props.chartData.map(item => item.value || 0))
  return max === 0 ? 1000 : max * 1.2
})

const chartSeries = computed(() => {
  return [
    {
      name: 'Затраты',
      data: props.chartData.map(item => item.value || 0)
    }
  ]
})

const chartOptions = computed(() => {
  return {
    chart: {
      type: 'area',
      height: 220,
      toolbar: { show: false },
      background: 'transparent',
      fontFamily: 'inherit',
      // Важно для правильного ресайза
      redrawOnParentResize: true,
      redrawOnWindowResize: true,
    },
    theme: {
      mode: 'dark',
    },
    colors: ['#a855f7'],
    stroke: {
      curve: 'smooth',
      width: 3,
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [0, 100]
      }
    },
    markers: {
      size: 4,
      colors: ['#1a1a1f'],
      strokeColors: '#a855f7',
      strokeWidth: 2,
      hover: { size: 6 }
    },
    dataLabels: { enabled: false },
    grid: {
      borderColor: 'rgba(255, 255, 255, 0.08)',
      strokeDashArray: 4,
      padding: {
        top: 0,
        right: 0,
        bottom: 0,
        left: 10
      },
      xaxis: { lines: { show: false } },
      yaxis: { lines: { show: true } }
    },
    xaxis: {
      categories: props.chartData.map(item => item.label),
      axisBorder: { show: false },
      axisTicks: { show: false },
      labels: {
        style: {
          colors: '#8a8a93',
          fontSize: '11px',
          fontWeight: 500
        },
        offsetY: 5
      },
      tooltip: { enabled: false }
    },
    yaxis: {
      max: maxValue.value,
      labels: {
        style: {
          colors: '#8a8a93',
          fontSize: '11px',
        },
        formatter: (value) => {
          if (value === 0) return '0'
          return Math.round(value).toLocaleString('ru-RU') + ' ₽'
        }
      },
    },
    tooltip: {
      theme: 'dark',
      x: { show: true },
      y: {
        formatter: (value) => `${value.toLocaleString('ru-RU')} ₽`,
        title: { formatter: () => 'Затраты:' }
      },
      marker: { show: true },
    },
    legend: { show: false }
  }
})
</script>

<style scoped>
.maintenance-cost-chart {
  width: 100%;
  min-width: 0;
  min-height: 220px; /* Обязательно, чтобы контейнер не схлопывался в 0 */
  position: relative;
}

.chart-box {
  width: 100%;
  min-width: 0;
}

/* Перекрашиваем тултипы ApexCharts под темную тему */
:deep(.apexcharts-tooltip) {
  background: #1e1e24 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
  border-radius: 6px !important;
}

:deep(.apexcharts-tooltip-title) {
  background: #2a2a35 !important;
  border-bottom: 1px solid rgba(255,255,255,0.1) !important;
}

.no-data {
  height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  font-size: 14px;
  gap: 8px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: var(--radius-md);
  border: 1px dashed var(--color-border);
}

.no-data i {
  font-size: 24px;
  opacity: 0.5;
}
</style>
