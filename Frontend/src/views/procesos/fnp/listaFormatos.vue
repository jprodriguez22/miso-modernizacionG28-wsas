<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';

import { cargarListaFNP } from './networkFunctions';

const headers = ref([
    { title: 'ID', key: 'IDFNP', align: 'start', sortable: true },
    { title: 'Proyecto', key: 'Proyecto', align: 'start', sortable: true },
    { title: 'Cliente', key: 'Cliente', align: 'start', sortable: true },
    { title: 'Título', key: 'Nombre', align: 'start', sortable: true},
    { title: 'ZFER', key: 'ZFER', align: 'start', sortable: true },
    { title: '', key: 'actions', align: 'end', sortable: true },
])

const rawItems = ref(null)

const items = ref([])

onMounted(async () => {
    //await actualizarPlanos()
    items.value = await cargarListaFNP()
})

</script>

<template>
    <p id="app-title">LISTA DE NOTIFICACIONES DE PRODUCTO</p>

    <v-row class="row-load-fnp">
        <v-col cols="2">
            <RouterLink :to="{ name: 'crearFNP' }">
                <v-btn color="success" id="btn-carga-fnp">
                    Nuevo FNP
                </v-btn>
            </RouterLink>
        </v-col>
    </v-row>
    <p>{{ rawItems }}</p>
    <v-row class="row-list-fnp">
        <v-col cols="12">
            <v-data-table :items="items" :headers="headers" class="elevation-1">
                <template v-slot:item.actions="{ item }">
                    <RouterLink class="button-link" :to="{ name: 'detalleFNP', query: { id: item.id } }">
                        <v-btn color="primary">
                            Capacitaciones
                        </v-btn>
                    </RouterLink>
                </template>
            </v-data-table>
        </v-col>
    </v-row>


</template>

<style>
.button-link {
    color: #2e2e2e;
    text-decoration: none;
}

.v-col {
    margin: 0;
    padding: 0;
}

.row-load-fnp {
    margin-top: 1.25rem;
    margin-left: 1.25rem;
    margin-right: 1.25rem;
    margin-bottom: 1.25rem;
    padding: 0.25rem;
}

.row-list-fnp {
    margin-top: 1.25rem;
    margin-left: 1.25rem;
    margin-right: 1.25rem;
    margin-bottom: 1.25rem;
    padding: 0.25rem;
}
</style>