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
                { month: 'Янв', count: 2 },
                { month: 'Фев', count: 1 },
                { month: 'Мар', count: 3 },
                { month: 'Апр', count: 1 },
                { month: 'Май', count: 2 },
                { month: 'Июн', count: 2 },
                { month: 'Июл', count: 4 },
                { month: 'Авг', count: 1 },
                { month: 'Сен', count: 3 },
                { month: 'Окт', count: 1 },
                { month: 'Ноя', count: 2 },
                { month: 'Дек', count: 3 }
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
                    background: 'transparent',
                },
                title: {
                    text: 'Кол-во обслуживаний',
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
                        text: 'Кол-во',
                        style: {
                            fontWeight: 500
                        }
                    },
                    labels: {
                        formatter: function(value) {
                            return value
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: function(value) {
                            return value
                        }
                    },
                    custom: function({ series, seriesIndex, dataPointIndex, w }) {
                        const month = w.globals.labels[dataPointIndex]
                        const count = w.config.series[0].data[dataPointIndex]
                        return `
                            <div style="padding: 10px;">
                                <strong>${month}</strong><br/>
                                Количество обслуживаний: ${count}
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
                    name: 'Количество обслуживаний',
                    data: this.chartData.map(item => item.count)
                }
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