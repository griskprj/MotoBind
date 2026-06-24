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
        maintenanceData: {
            type: Array,
            default: () => []
        }
    },

    data() {
        return {
            chartData: [
                { month: 'Янв', cost: 1200, count: 2 },
                { month: 'Фев', cost: 800, count: 1 },
                { month: 'Мар', cost: 2400, count: 3 },
                { month: 'Апр', cost: 600, count: 1 },
                { month: 'Май', cost: 1800, count: 2 },
                { month: 'Июн', cost: 1500, count: 2 },
                { month: 'Июл', cost: 3000, count: 4 },
                { month: 'Авг', cost: 900, count: 1 },
                { month: 'Сен', cost: 2100, count: 3 },
                { month: 'Окт', cost: 700, count: 1 },
                { month: 'Ноя', cost: 1600, count: 2 },
                { month: 'Дек', cost: 2500, count: 3 }
            ]
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
                title: {
                    text: 'Стоимость обслуживаний',
                    align: 'center',
                    margin: 10,
                    offsetX: 0,
                    offsetY: 0,
                    floating: false,
                    style: {
                        fontSize: '18px',
                        fontWeight: 'bold',
                        fontFamily: 'inherit',
                        color: '#333'
                    }
                },
                plotOptions: {
                    bar: {
                        borderRadius: 8,
                        columnWidth: '60%',
                        distribured: false
                    }
                },
                colors: ['#7C3AED', '#2D2A3E'],
                dataLabels: {
                    enabled: false
                },
                grid: {
                    borderColor: '#2D2D3A',
                    row: {
                        colors: ['#64748B', 'transparent'],
                        opasity: 0.5
                    }
                },
                xaxis: {
                    categories: this.chartData.map(item => item.month),
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
                    },
                    custom: function({ series, seriesIndex, dataPointIndex, w }) {
                        const month = w.globals.labels[dataPointIndex]
                        const cost = series[0][dataPointIndex]
                        return `
                            <div style="padding: 10px;">
                                <strong>${month}</strong><br/>
                                Затраты: ${cost} ₽<br/>
                            </div>
                        `
                    }
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'center',
                    labels: {
                        colors: '#333'
                    }
                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            height: 300
                        },
                        plotOptions: {
                            bar: {
                                columnWidth: '80%'
                            }
                        }
                    }
                }]
            }
        },
        chartSeries() {
            return [
                {
                    name: 'Затраты на обслуживание',
                    data: this.chartData.map(item => item.cost)
                },
            ]
        }
    },

    mounted() {
        if (this.maintenanceData && this.maintenanceData.length > 0) {
            this.chartData = this.maintenanceData
        }
    },

    watch: {
        maintenanceData: {
            handler(newData) {
                if (newData && newData.length > 0) {
                    this.chartData = newData
                }
            },
            deep: true
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