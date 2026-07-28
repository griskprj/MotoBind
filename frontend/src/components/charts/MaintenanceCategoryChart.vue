<template>
    <div class="maintenance-category-chart">
        <apexchart
            v-if="chartData && chartData.length > 0"
            :options="chartOptions"
            :series="chartSeries"
            height="350"
            type="donut"
        />
        <div v-else class="no-data">
            <p>Нет данных по категориям</p>
        </div>
    </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'

export default {
    name: 'MaintenanceCategoryChart',
    components: {
        apexchart: VueApexCharts
    },

    props: {
        // Ожидаем массив объектов: [{ category: "Расходники", cost: 36000 }, ...]
        chartData: {
            type: Array,
            default: () => []
        }
    },

    computed: {
        // Вычисляем общую сумму для отображения в центре
        totalCost() {
            if (!this.chartData || this.chartData.length === 0) return 0;
            return this.chartData.reduce((sum, item) => sum + (item.cost || 0), 0);
        },

        chartOptions() {
            return {
                chart: {
                    type: 'donut',
                    height: 350,
                    background: 'transparent'
                },
                // Цвета подбираем под дизайн (как на скрине)
                colors: ['#7C3AED', '#3B82F6', '#22C55E', '#EAB308', '#EF4444', '#8B8B9E'],
                labels: this.chartData.map(item => item.category || 'Категория'),
                
                // Настройки кольца (чтобы внутри был текст)
                plotOptions: {
                    pie: {
                        donut: {
                            size: '65%',
                            labels: {
                                show: true,
                                name: {
                                    show: false
                                },
                                value: {
                                    show: true,
                                    fontSize: '22px',
                                    fontFamily: 'Inter, sans-serif',
                                    fontWeight: 700,
                                    color: '#ffffff',
                                    offsetY: -10,
                                    formatter: function(val) {
                                        return val.toLocaleString() + ' ₽'
                                    }
                                },
                                total: {
                                    show: true,
                                    showAlways: true,
                                    label: 'Всего',
                                    fontSize: '14px',
                                    fontFamily: 'Inter, sans-serif',
                                    fontWeight: 400,
                                    color: '#8b8b9e',
                                    formatter: function() {
                                        return this.w.globals.seriesTotals.reduce((a, b) => a + b, 0).toLocaleString() + ' ₽'
                                    }
                                }
                            }
                        }
                    }
                },
                
                // Легенда справа с процентами
                legend: {
                    position: 'right',
                    verticalAlign: 'middle',
                    height: 280,
                    offsetY: 0,
                    labels: {
                        colors: '#d1d1d1', // Цвет текста легенды
                        useSeriesColors: false
                    },
                    markers: {
                        width: 12,
                        height: 12,
                        radius: 4
                    },
                    formatter: function(seriesName, opts) {
                        // Опция для отображения процентов рядом с названием
                        return seriesName + "  <span style='color:#8b8b9e; margin-left:8px;'>" + opts.w.globals.series[opts.seriesIndex] + "%</span>"
                    }
                },
                
                // Настройки данных на графике (чтобы не было подписей на кусках)
                dataLabels: {
                    enabled: false
                },
                
                // Всплывающие подсказки
                tooltip: {
                    y: {
                        formatter: function(value) {
                            return value.toLocaleString() + ' ₽'
                        }
                    }
                },
                
                // Адаптивность
                responsive: [{
                    breakpoint: 768,
                    options: {
                        chart: {
                            height: 300
                        },
                        legend: {
                            position: 'bottom',
                            verticalAlign: 'bottom',
                            height: 150
                        }
                    }
                }]
            }
        },

        // Данные для самой диаграммы (только цифры)
        chartSeries() {
            return this.chartData.map(item => item.cost || 0)
        }
    }
}
</script>

<style scoped>
.maintenance-category-chart {
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
    .maintenance-category-chart {
        padding: 12px;
    }
}
</style>