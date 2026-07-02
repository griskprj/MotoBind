<template>
    <div class="maintenance-cost-chart">
        <apexchart
            v-if="chartData && chartData.length > 0"
            :options="chartOptions"
            :series="chartSeries"
            height="350"
            type="line"
        />
        <div v-else class="no-data">
            <p>Нет данных для отображения</p>
        </div>
    </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'

export default {
    name: 'MaintenanceCostChart',
    components: {
        apexchart: VueApexCharts
    },

    props: {
        chartData: {
            type: Array,
            default: () => []
        }
    },

    computed: {
        chartOptions() {
            return {
                chart: {
                    type: 'line',
                    height: 350,
                    toolbar: {
                        show: true,
                        tools: {
                            download: true,
                            selection: true,
                            zoom: true,
                            zoomin: false,
                            zoomout: false,
                            pan: false,
                            reset: true
                        }
                    },
                    background: 'transparent'
                },
                stroke: {
                    curve: 'smooth',
                    width: 3
                },
                markers: {
                    size: 5,
                    colors: ['#7C3AED'],
                    strokeColors: '#fff',
                    strokeWidth: 2,
                    hover: {
                        size: 7
                    }
                },
                colors: ['#7C3AED'],
                dataLabels: {
                    enabled: false
                },
                grid: {
                    borderColor: '#e0e0e0',
                    row: {
                        colors: ['transparent'],
                        opacity: 0.5
                    }
                },
                xaxis: {
                    categories: this.chartData.map(item => item.month || item.date),
                    title: {
                        text: 'Месяц',
                        style: {
                            fontWeight: 500
                        }
                    }
                },
                yaxis: {
                    title: {
                        text: 'Затраты (₽)',
                        style: {
                            fontWeight: 500
                        }
                    },
                    labels: {
                        formatter: function(value) {
                            return value + ' ₽'
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: function(value) {
                            return value + ' ₽'
                        }
                    }
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'center'
                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            height: 300
                        }
                    }
                }]
            }
        },
        
        chartSeries() {
            return [
                {
                    name: 'Затраты на обслуживание',
                    data: this.chartData.map(item => item.value || item.cost || 0)
                }
            ]
        }
    }
}
</script>

<style scoped>
.maintenance-cost-chart {
  width: 100%;
  max-width: 800px;
  padding: 20px;
  background-color: var(--bg-secondary, #ffffff);
  border-radius: 16px;
  border: 1px solid var(--border-color, #e0e0e0);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.no-data {
  height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 16px;
}

@media (max-width: 768px) {
  .maintenance-cost-chart {
    padding: 12px;
  }
}
</style>