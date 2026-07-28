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
                        show: false,
                    },
                    background: 'transparent'
                },
                title: {
                    text: 'Затраты на обслуживания по месяцам',
                    align: 'center',
                    margin: 10,
                    style: {
                        fontSize: '18px',
                        fontWeight: 'bold',
                        fontFamily: 'inherit',
                        color: '#333'
                    }
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
  padding: 0;
  background-color: transparent;
  border: none;
  box-shadow: none;
}

.no-data {
  height: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 16px;
}

@media (max-width: 768px) {
  .maintenance-cost-chart {
    padding: 12px;
  }
}
</style>