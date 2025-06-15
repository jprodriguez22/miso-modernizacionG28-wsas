<script>
import VueApexCharts from 'vue3-apexcharts';

export default {
    name: 'Chart',
    components: {
        apexcharts: VueApexCharts,
    },
    props: {
        xdata: {
            type: Array,
            required: true,
        },
        ydata: {
            type: Array,
            required: true,
        }
    },
    data() {
        return {
            chartOptions: {
                annotations: {
                    yaxis: [
                        {
                            y: 25,
                            borderColor: '#EF4C4C',
                            label: {
                                borderColor: '#EF4C4C',
                                style: {
                                    color: '#fff',
                                    background: '#EF4C4C'
                                },
                                text: 'Temperatura máxima'
                            }
                        }
                    ]
                },
                chart: {
                    id: 'basic-line',
                    type: 'line',
                    zoom: { enabled: true }
                },
                fill: {
                    colors: ['#8fc5cf'],
                },
                stroke: { curve: 'straight' },
                title: { text: 'Condiciones de cuarto', align: 'center' },
                xaxis: {
                    categories: [],
                    tickAmount: 18,
                    type: 'datetime'
                },
                yaxis: {
                    labels: {
                        formatter: val => val.toFixed(1)
                    }
                }
            },
            chartSeries: [
                {
                    name: "Condiciones",
                    data: [],
                },
            ]
        };
    },
    
    watch: {
        xdata: {
            handler(newXData) {
                if (newXData) {
                    this.chartOptions.xaxis.categories = newXData;
                }
            },
        },
        ydata: {
            handler(newYData) {
                if (newYData) {
                    this.chartSeries[0].data = newYData;
                }
            },
        }
    },
};
</script>

<template>
    <div class="chart" v-if="xdata && ydata">
        <apexchart style="display: flex" type="line" :options="chartOptions" :series="chartSeries"></apexchart>
    </div>
    <div v-else>
        <!-- Optionally, you can add a loading indicator or some other message here -->
        Loading data...
    </div>
</template>
  