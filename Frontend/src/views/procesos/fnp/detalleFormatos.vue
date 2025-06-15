<script setup>
import { ref, onMounted, onBeforeMount, watch } from 'vue';
import { RouterLink } from 'vue-router';

import workStations from '../../../configuration/workStations.json'

const props = defineProps({
    id: {
        type: Number,
        required: true
    }
})

const id = ref(0)
const client = ref('Indikar Individual Karosseriebau GmBH')
const project = ref('Land Rover Sentinel 4D Utility')
const listZFER = ref(['700156147', '700156148', '700156149', '700156150', '700156151'])
const activeTab = ref('1-Corte')
const List1 = ['Pepito Perez', 'Sutanita Mendoza', 'Jairo Martinez', 'Clara Valencia']
const List2 = ['Dario Lopez', 'Camilo Cespedes', 'Juana de los ángeles']
const workerList = ref([])

onBeforeMount(() => {
    updateWorkerList()
})

onMounted(() => {
    id.value = props.id
})

function updateWorkerList(station){
    if (station === '2-Mecanizado'){
        workerList.value = List2
    }
    else {
        workerList.value = List1
    }
}

watch(activeTab, (station) => {
    updateWorkerList(station)
})

</script>

<template>
    <p id="app-title">DETALLE DE NOTIFICACIÓN DE PRODUCTO</p>

    <v-row>

        <v-col cols="5">
            <v-row class="row-back-button">
                <v-col cols="1">
                    <RouterLink class="button-link" :to="{ name: 'listaFNP' }">
                        <v-tab color="accent" id="btn-return">
                            VOLVER
                        </v-tab>
                    </RouterLink>
                </v-col>
            </v-row>
            <v-row class="row-card-details" v-if="id">
                <v-col>
                    <v-card :title="`FNP-${id}`">
                        <v-card-text>
                            <p><b>Cliente: </b>{{ client }}</p>
                            <p><b>Proyecto: </b>{{ project }}</p>
                            <p><b>ZFER:</b></p>
                            <ul v-if="listZFER">
                                <li v-for="item in listZFER">
                                    {{ item }}
                                </li>
                            </ul>
                        </v-card-text>

                        <v-card-actions>
                            <v-btn class="common-button">Editar</v-btn>
                            <v-btn class="common-button">Borrar</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>

        <v-col cols="7">
            <v-row class="row-trained-personal" id="trained-workers-card">
                <v-card>
                    <v-tabs v-model="activeTab" align-tabs="center" color="accent" center-active
                        next-icon="mdi-arrow-right" prev-icon="mdi-arrow-left" show-arrows>
                        <v-tab v-for="station in workStations" :key="station" :text="station" :value="station">
                        </v-tab>
                    </v-tabs>

                    <v-card-text>
                        <v-row class="row-trained-personal-body" align="center">
                            <v-col cols="1">
                                <v-icon icon="mdi-briefcase" color="primary" size="40"></v-icon>
                            </v-col>
                            <v-col cols="7">
                                <p id="trained-workers-title">Personal entrenado</p>
                            </v-col>
                            <v-col cols="4">
                                <RouterLink class="button-link" :to="{ name: 'capacitarPersonal', query: { id: props.id } }">
                                    <v-btn color="primary" class="common-button">Agregar personas</v-btn>
                                </RouterLink>
                            </v-col>
                        </v-row>
                        <v-divider></v-divider>
                        <v-row class="row-trained-personal-body-list" v-for="worker in workerList">
                            <v-col cols="1">
                                <v-icon icon="mdi-account" color="accent" size="24"></v-icon>
                            </v-col>
                            <v-col>
                                <p>{{ worker }}</p>
                            </v-col>
                        </v-row>
                    </v-card-text>

                </v-card>
            </v-row>
        </v-col>

    </v-row>

</template>

<style>
.button-link {
    color: #2e2e2e;
    text-decoration: none;
}

.common-button {
    font-size: 100% !important;
}

.row-back-button {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-card-details {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-trained-personal {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-trained-personal-body {
    margin: 0.5rem;
}

.row-trained-personal-body-list {
    margin: 0.625rem 0.5rem;
}

#btn-return {
    border-bottom: solid;
    border-radius: 0.25rem;
    height: 3rem;
}

#trained-workers-title {
    font-size: 1.25rem !important;
    font-weight: bold;
    margin: 0 0 0 1.25rem;
    text-align: left;
}

</style>