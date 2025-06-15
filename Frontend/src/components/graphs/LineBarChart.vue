<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
    name: 'Chart',
    components: {
        apexcharts: VueApexCharts,
    },
    props: {
        xdata: {
            required: true,
        },
        ydataLine: {
            required: true,
        },
        ydataBar: {
            required: true,
        },
        chartTitle: {
            type: String,
            required: false,
        }
    },
    data() {
        return {
            series: [{
                name: "Eventos",
                type: 'column',
                data: [],
            },
            {
                name: "Impacto al costo",
                type: 'line',
                data: [],
            }
            ],

            chartOptions: {
                chart: {
                    id: 'line-bar-chart',
                    type: 'line',
                    zoom: { enabled: false }
                },
                colors: ['#8fc5cf', '#2F2D2E'],
                fill: {
                    colors: ['#8fc5cf'],
                },
                markers: {
                    size: [0, 4]
                },
                stroke: { 
                    curve: 'straight', 
                    colors: ['#2F2D2E'],
                    width: 1,                
                },
                dataLabels: {
                    enabled: true,
                    enabledOnSeries: [0, 1],
                    style: {
                        colors: ['#48636A', '#2F2D2E']
                    }
                },
                xaxis: {
                    categories: [],
                    labels: {
                        rotate: 0,
                        rotateAlways: false,
                        trim: true,
                        hideOverlappingLabels: false
                    },
                },
                yaxis: [
                    {
                        title: {
                            text: 'Cantidad de eventos'
                        },
                    },
                    {
                        opposite: true,
                        title: {
                            text: 'Porcentaje de impacto'
                        }
                    }
                ]
            },
        };
    },

    watch: {
        xdata: {
            handler(newXData) {
                if (newXData) {
                    this.updateCategories(newXData);
                }
            },
        },
        ydataBar: {
            handler(newYBar) {
                if (newYBar) {
                    this.series[0].data = newYBar;
                }
            }
        },
        ydataLine: {
            handler(newYLine) {
                if (newYLine) {
                    this.series[1].data = newYLine;
                }
            },
        },
        chartTitle: {
            handler(newTitle) {
                if (newTitle) {
                    this.updateTitle(newTitle);
                }
            },
        }
    },
    methods: {
        updateCategories(newXData) {
            this.chartOptions = {
                ...this.chartOptions,
                xaxis: {
                    ...this.chartOptions.xaxis,
                    categories: newXData
                }
            };
        }
    }
};
</script>

<template>
    <div class="chart" v-if="xdata && ydataBar && ydataLine">
        <p class="chart-title">{{ chartTitle }}</p>
        <apexchart ref="chart" style="display: flex" type="line" :options="chartOptions" :series="series"></apexchart>
    </div>
    <div v-else>
        <VueSpinnerOval class="loading-screen-ovalspinner" size="60" color="#5F7A83"></VueSpinnerOval>
    </div>
</template>

<style>
    .chart-title {
        font-size: 0.9rem !important;
        font-weight: bold;
        line-height: 2rem;
        margin: 0;
        text-align: center;
    }
    .loading-screen-ovalspinner {
        margin: auto;
        min-height: 50vh;
    }
</style>