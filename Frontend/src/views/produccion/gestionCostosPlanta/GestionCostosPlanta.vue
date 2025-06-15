<script setup>
// Importing
import { computed, ref, onBeforeMount, watch } from 'vue';
import { ModalsContainer, VueFinalModal } from 'vue-final-modal';
import { RouterLink } from 'vue-router';
import { Field } from 'vee-validate';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

import LineBarChart from '../../../components/graphs/LineBarChart.vue'

import { loadDataset, calculateYield, overpricedCount, calculateExcessMoney, calculateOvercostRelation, countActiveOrders, loadOrderDetailsByDefect, loadOrderDetailsByOrigin } from './functions';
import { filterDataset, sortTableBy, searchOnFilter } from './filterFunctions';
import { defineDivBackground } from './functions';

// Primary variables initialization
const fullDataset = ref(null) // This is the dataset for the entire dashboard
const selectedOrderInfo = ref(null) // Contains the info form the selected order from the base dataset
const orderDetailsDefect = ref([]) // This dataset contains the history of rejections grouped by defects for the selected order
const orderDetailsOrigin = ref([]) // This dataset contains the history of rejections grouped by origin for the selected order
const overpricedPieces = ref(null) // Refers to the count of pieces which have a relation of 2 or bigger
const yieldCalculation = ref(null) // This is yield calculation depending on the selected filters
const excessMoney = ref(0) // This is the diference between final costs and planned costs
const overcostRate = ref(0) // Rate of the overcost
const activeOrders = ref(0) // Number of orders that are on the current dataset

const activeDataset = computed(() => {
    if (fullDataset.value) {
        return filterDataset(
            fullDataset.value,
            filterComplex.value,
            filterMarket.value,
            filterBlock.value,
            filterLevel.value,
            filterFormula.value,
            filterOverprice.value,
            filterArea.value,
            filterClient.value,
            filterVehicle.value,
            orderSearchBar.value,
            zferSearchBar.value
        )
    }
    else {
        return null
    }
})

// Filter variables initialization
const filterComplex = ref("")
const filterMarket = ref("")
const filterBlock = ref("")
const filterLevel = ref("")
const filterFormula = ref("")
const filterOverprice = ref("")
const filterArea = ref("")
const filterClient = ref("")
const filterVehicle = ref("")
const sortOrder = ref("DESCENDING")
const sortHeader = ref("RelacionSobrecosto")

// CSS variables
const divBackground = ref("clear-background")

// Lists for the dropdown filters
const listMarkets = ref(null)
const listLevels = ref(null)
const listFormulas = ref(null)
const listAreas = ref(null)
const listClients = ref(null)
const listBlocks = ref(null)
const listVehicles = ref(null)

// Input fields to search on filters
const clientSearchBar = ref("")
const vehicleSearchBar = ref("")
const formulaSearchBar = ref("")
const orderSearchBar = ref("")
const zferSearchBar = ref("")

// Application Lifecycle
onBeforeMount(async () => {
    fullDataset.value = await loadDataset()
    listMarkets.value = searchOnFilter('', 'Mercado', fullDataset.value)
    listLevels.value = searchOnFilter('', 'Nivel', fullDataset.value)
    listFormulas.value = searchOnFilter('', 'Formula', fullDataset.value)
    listAreas.value = searchOnFilter('', 'Puestodetrabajo', fullDataset.value)
    listClients.value = searchOnFilter('', 'Cliente', fullDataset.value)
    listBlocks.value = searchOnFilter('', 'Bloque', fullDataset.value)
    listVehicles.value = searchOnFilter('', 'Vehiculo', fullDataset.value)
})

// Watchers for measures
watch(activeDataset, (dataset) => {
    if (dataset) {
        yieldCalculation.value = calculateYield(dataset)
        overpricedPieces.value = overpricedCount(dataset)
        excessMoney.value = calculateExcessMoney(dataset)
        overcostRate.value = calculateOvercostRelation(dataset)
        activeOrders.value = countActiveOrders(dataset)
    }
})

watch(yieldCalculation, (value) => {
    divBackground.value = defineDivBackground(value)
})

// Watchers for filters

watch(clientSearchBar, (input) => {
    listClients.value = searchOnFilter(input, "Cliente", fullDataset.value)
})

watch(formulaSearchBar, (input) => {
    listFormulas.value = searchOnFilter(input, "Formula", fullDataset.value)
})

watch(vehicleSearchBar, (input) => {
    listVehicles.value = searchOnFilter(input, "Vehiculo", fullDataset.value)
})

// Local variable functions
async function loadOrderDetailDefectVariable(order) {
    orderDetailsDefect.value = await loadOrderDetailsByDefect(order)
}

async function loadOrderDetailOriginVariable(order) {
    orderDetailsOrigin.value = await loadOrderDetailsByOrigin(order)
}

function cleanDetailVariables() {
    orderDetailsDefect.value = []
    orderDetailsOrigin.value = []
}

function resetFilters() {
    try {
        filterComplex.value = ""
        filterMarket.value = ""
        filterBlock.value = ""
        filterLevel.value = ""
        filterFormula.value = ""
        filterOverprice.value = ""
        filterArea.value = ""
        filterClient.value = ""
        filterVehicle.value = ""
        orderSearchBar.value = ""
        zferSearchBar.value = ""
        formulaSearchBar.value = ""
        clientSearchBar.value = ""
        vehicleSearchBar.value = ""
        toast("Se han reiniciado los filtros", {
            "type": "info",
            "position": "bottom-right",
            "dangerouslyHTMLString": true,
            "pauseOnFocusLoss": false,
        }
        )
    }
    catch {
        toast("Ha habido un error durante la operación solicitada", {
            "type": "error",
            "position": "bottom-right",
            "dangerouslyHTMLString": true,
            "pauseOnFocusLoss": false,
        }
        )
    }
}

async function refreshData() {
    try {
        fullDataset.value = null
        fullDataset.value = await loadDataset()
        sortHeader.value = "RelacionSobrecosto"
        sortOrder.value = "DESCENDING"
        toast("Datos actualizados satisfactoriamente", {
            "type": "success",
            "position": "bottom-right",
            "dangerouslyHTMLString": true,
        }
        )
    }
    catch {
        toast("Ha habido un error durante la operación solicitada", {
            "type": "error",
            "position": "bottom-right",
            "dangerouslyHTMLString": true,
        }
        )
    }
}

function sortTableOnClick(header) {
    if (header === sortHeader.value) {
        if (sortOrder.value === 'DESCENDING') {
            sortOrder.value = 'ASCENDING'
        }
        else {
            sortOrder.value = 'DESCENDING'
        }
    }
    sortHeader.value = header
    activeDataset.value = sortTableBy(activeDataset.value, sortHeader.value, sortOrder.value)
}

function loadOrderDetails(data) {
    loadOrderDetailDefectVariable(data.Orden)
    loadOrderDetailOriginVariable(data.Orden)
    options.value.modelValue = true
    selectedOrderInfo.value = data
}

// Modal Parameters
const getInitialValues = () => ({
    teleportTo: 'body',
    modelValue: false,
    modelReportValue: false,
    displayDirective: 'if',
    hideOverlay: true,
    overlayTransition: 'vfm-fade',
    contentTransition: 'vfm-fade',
    clickToClose: false,
    escToClose: true,
    background: 'non-interactive',
    lockScroll: true,
    reserveScrollBarGap: true,
    swipeToClose: 'none',
})

const options = ref(getInitialValues())

</script>

<template>
    <p id="app-title">COSTO DE PIEZAS EN PRODUCCIÓN</p>

    <div class="fullpage-loading-screen" v-if="!fullDataset">
        <VueSpinnerOval class="loading-screen-ovalspinner" size="60" color="#5F7A83"></VueSpinnerOval>
    </div>

    <div class="row" id="dashboard-body">

        <div class="col col-2" id="dashboard-filter-column">

            <button type="button" class="btn btn-dark context-button" v-on:click="refreshData()"><img
                    src="/synchronize.svg" class="context-button-icon" id="reset-filters-icon">Actualizar datos</button>

            <button type="button" class="btn btn-dark context-button" v-on:click="resetFilters()"><img
                    src="/recycle-bin.svg" class="context-button-icon" id="reset-filters-icon">Reiniciar
                filtros</button>

            <label class="dashboard-filter-label col col-10">Complejidad</label>
            <img src="/recycle-bin.svg" v-on:click="filterComplex = ''" class="clean-filter-icon col col-2">
            <div class="dashboard-radio-filter-body" id="dashboard-filter-complex">
                <input title="Retrofit Filter" name="dashboard-filter-complex" id="retrofit-radio-filter" type="radio"
                    class="dashboard-filter-radio" value="0" v-model="filterComplex" />
                <label for="retrofit-radio-filter" class="dashboard-filter-radio-label">Retrofit</label>
                <input title="Complex Filter" name="dashboard-filter-complex" id="complex-radio-filter" type="radio"
                    class="dashboard-filter-radio" value="1" v-model="filterComplex" />
                <label for="complex-radio-filter" class="dashboard-filter-radio-label">Complex</label>
            </div>

            <label class="dashboard-filter-label col col-10">Sobrecosto</label>
            <img src="/recycle-bin.svg" v-on:click="filterOverprice = ''" class="clean-filter-icon col col-2">
            <div class="dashboard-radio-filter-body">
                <input title="Retrofit Filter" name="dashboard-filter-overprice" id="overprice-radio-yes" type="radio"
                    class="dashboard-filter-radio" value="1" v-model="filterOverprice" />
                <label for="overprice-radio-yes" class="dashboard-filter-radio-label">Si</label>
                <input title="Complex Filter" name="dashboard-filter-overprice" id="overprice-radio-no" type="radio"
                    class="dashboard-filter-radio" value="0" v-model="filterOverprice" />
                <label for="overprice-radio-no" class="dashboard-filter-radio-label">No</label>
            </div>

            <label for="dashboard-filter-order" class="dashboard-filter-label col col-10">Orden</label>
            <img src="/recycle-bin.svg" v-on:click="orderSearchBar = ''" class="clean-filter-icon col col-2">
            <Field class="dashboard-filter-search" title="Order filter search bar" type="number" min="0" step="1"
                name="dashboard-filter-order-search" as="input" placeholder="Buscar" v-model="orderSearchBar" id="dashboard-filter-order">
            </Field>

            <label for="dashboard-filter-ZFER" class="dashboard-filter-label col col-10">ZFER</label>
            <img src="/recycle-bin.svg" v-on:click="zferSearchBar = ''" class="clean-filter-icon col col-2">
            <Field class="dashboard-filter-search" title="ZFER filter search bar" type="number" min="0.000001"
                name="dashboard-filter-ZFER-search" as="input" placeholder="Buscar" v-model="zferSearchBar" id="dashboard-filter-ZFER">
            </Field>


            <label for="dashboard-filter-market" class="dashboard-filter-label col col-10">Mercado</label>
            <img src="/recycle-bin.svg" v-on:click="filterMarket = ['']" class="clean-filter-icon col col-2">
            <Field v-model="filterMarket" title="Market Filter" name="dashboard-filter-market"
                id="dashboard-filter-market" as="select" class="dashboard-filter-select" multiple>
                <option v-for="market in listMarkets" :value="market">
                    {{ market }}
                </option>
            </Field>

            <label for="dashboard-filter-block" class="dashboard-filter-label col col-10">Bloque</label>
            <img src="/recycle-bin.svg" v-on:click="filterBlock = ['']" class="clean-filter-icon col col-2">
            <Field v-model="filterBlock" title="Block Filter" name="dashboard-filter-block" id="dashboard-filter-block"
                as="select" class="dashboard-filter-select" multiple>
                <option v-for="block in listBlocks" :value="block">
                    {{ block }}
                </option>
            </Field>

            <label for="dashboard-filter-level" class="dashboard-filter-label col col-10">Nivel</label>
            <img src="/recycle-bin.svg" v-on:click="filterLevel = ['']" class="clean-filter-icon col col-2">
            <Field v-model="filterLevel" title="Level Filter" name="dashboard-filter-level" id="dashboard-filter-level"
                as="select" class="dashboard-filter-select" multiple>
                <option v-for="level in listLevels" :value="level">
                    {{ level }}
                </option>
            </Field>

            <label for="dashboard-filter-formula" class="dashboard-filter-label col col-10">Fórmula</label>
            <img src="/recycle-bin.svg" v-on:click="filterFormula = ['']" class="clean-filter-icon col col-2">
            <Field class="dashboard-filter-search" title="Formula filter search bar"
                name="dashboard-filter-formula-search" as="input" placeholder="Buscar" v-model="formulaSearchBar">
            </Field>
            <Field v-model="filterFormula" title="Formula Filter" name="dashboard-filter-formula"
                id="dashboard-filter-formula" as="select" class="dashboard-filter-select" multiple>
                <option v-for="formula in listFormulas" :value="formula">
                    {{ formula }}
                </option>
            </Field>

            <label for="dashboard-filter-area" class="dashboard-filter-label col col-10">Puesto de Trabajo</label>
            <img src="/recycle-bin.svg" v-on:click="filterArea = ['']" class="clean-filter-icon col col-2">
            <Field v-model="filterArea" title="Area Filter" name="dashboard-filter-area" id="dashboard-filter-area"
                as="select" class="dashboard-filter-select" multiple>
                <option v-for="area in listAreas" :value="area">
                    {{ area }}
                </option>
            </Field>

            <label for="dashboard-filter-client" class="dashboard-filter-label col col-10">Cliente</label>
            <img src="/recycle-bin.svg" v-on:click="filterClient = ['']; clientSearchBar = ''"
                class="clean-filter-icon col col-2">
            <Field class="dashboard-filter-search" title="Client filter search bar"
                name="dashboard-filter-client-search" as="input" placeholder="Buscar" v-model="clientSearchBar"></Field>
            <Field v-model="filterClient" title="Client Filter" name="dashboard-filter-client"
                id="dashboard-filter-client" as="select" class="dashboard-filter-select" multiple>
                <option v-for="client in listClients" :value="client">
                    {{ client }}
                </option>
            </Field>

            <label for="dashboard-filter-vehicle" class="dashboard-filter-label col col-10">Vehículo</label>
            <img src="/recycle-bin.svg" v-on:click="filterVehicle = ['']" class="clean-filter-icon col col-2">
            <Field class="dashboard-filter-search" title="Vehicle filter search bar"
                name="dashboard-filter-vehicle-search" as="input" placeholder="Buscar" v-model="vehicleSearchBar">
            </Field>
            <Field v-model="filterVehicle" title="Vehicle Filter" name="dashboard-filter-vehicle"
                id="dashboard-filter-vehicle" as="select" class="dashboard-filter-select" multiple>
                <option v-for="vehicle in listVehicles" :value="vehicle">
                    {{ vehicle }}
                </option>
            </Field>

        </div>

        <div class="col col-10" id="dashboard-graph-column">

            <div class="row" id="dashboard-graph-measures">
                <div class="col col-1 measure">
                    <div class="measure-header">
                        <p class="measure-header-title">Yield</p>
                    </div>
                    <div :class="`measure-body ${divBackground}`">
                        <p class="measure-body-content">{{ yieldCalculation }}%</p>
                    </div>
                </div>

                <div class="col col-1 measure">
                    <div class="measure-header">
                        <p class="measure-header-title">Total de ordenes</p>
                    </div>
                    <div class="measure-body">
                        <p class="measure-body-content">{{ activeOrders }}</p>
                    </div>
                </div>

                <div class="col col-1 measure">
                    <div class="measure-header">
                        <p class="measure-header-title">Ordenes sobrecosto</p>
                    </div>
                    <div class="measure-body">
                        <p class="measure-body-content">{{ overpricedPieces }}</p>
                    </div>
                </div>

                <div class="col col-1 measure">
                    <div class="measure-header">
                        <p class="measure-header-title">Sobrecosto [$USD]</p>
                    </div>
                    <div class="measure-body">
                        <p class="measure-body-content">$ {{ excessMoney }}</p>
                    </div>
                </div>

                <div class="col col-1 measure">
                    <div class="measure-header">
                        <p class="measure-header-title">Sobrecosto medio</p>
                    </div>
                    <div class="measure-body">
                        <p class="measure-body-content">{{ overcostRate }}</p>
                    </div>
                </div>

            </div>

            <div class="row" id="dashboard-graph-table">
                <table class="table table-hover align-middle">
                    <thead class="align-middle dataset-headers">
                        <tr>
                            <th scope="col">Detalle</th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Orden', sortHeader === `Orden` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Orden')">Orden</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-ZFER', sortHeader === `ZFER` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('ZFER')">ZFER</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Vehiculo', sortHeader === `Vehiculo` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Vehiculo')">Descripción</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-CodTipoPieza', sortHeader === `CodTipoPieza` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('CodTipoPieza')">Pieza</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Cliente', sortHeader === `Cliente` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Cliente')">Cliente</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Mercado', sortHeader === `Mercado` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Mercado')">Mercado</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Nivel', sortHeader === `Nivel` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Nivel')">Nivel</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Formula', sortHeader === `Formula` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Formula')">Formula</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-Puestodetrabajo', sortHeader === `Puestodetrabajo` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('Puestodetrabajo')">Puesto</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-KeyModel', sortHeader === `KeyModel` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('KeyModel')">Clave</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-HorasQuietas', sortHeader === `HorasQuietas` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('HorasQuietas')">Horas</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-CostoPlan', sortHeader === `CostoPlan` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('CostoPlan')">Plan</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-CostoReal', sortHeader === 'CostoReal' ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('CostoReal')">Real</a></th>
                            <th scope="col"><a href="#"
                                    :class="['table-filter-header', 'header-RelacionSobrecosto', sortHeader === `RelacionSobrecosto` ? `active-sort-${sortOrder}` : '']"
                                    v-on:click="sortTableOnClick('RelacionSobrecosto')">Sobrecosto</a></th>
                            <th scope="col">Lecciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="data in activeDataset" :key="data.Orden">
                            <td class="dataset-entry"
                                v-on:click="loadOrderDetails(data)">
                                <img src="\eyeball.svg" id="details-icon">
                            </td>
                            <td class="dataset-entry">{{ data.Orden }}</td>
                            <td class="dataset-entry">{{ data.ZFER }}</td>
                            <td class="dataset-entry">{{ data.Vehiculo }}</td>
                            <td class="dataset-entry">{{ data.CodTipoPieza }}</td>
                            <td class="dataset-entry">{{ data.Cliente }}</td>
                            <td class="dataset-entry">{{ data.Mercado }}</td>
                            <td class="dataset-entry">{{ data.Nivel }}</td>
                            <td class="dataset-entry">{{ data.Formula }}</td>
                            <td class="dataset-entry">{{ data.Puestodetrabajo }}</td>
                            <td class="dataset-entry">{{ data.KeyModel }}</td>
                            <td class="dataset-entry">{{ data.HorasQuietas }}</td>
                            <td class="dataset-entry">{{ data.CostoPlan }}</td>
                            <td class="dataset-entry">{{ data.CostoReal }}</td>
                            <td class="dataset-entry">{{ data.RelacionSobrecosto }}</td>
                            <td class="dataset-entry">
                                <RouterLink :to="{ name: 'leccionesAprendidas', query: {order: data.Orden} }">
                                    <img src="\eyeball.svg" id="details-icon">
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>

                </table>
            </div>
        </div>
    </div>

    <!-- Modal -->
    <div class="flex modal-background" v-if="options.modelValue">
        <VueFinalModal v-model="options.modelValue" :teleport-to="options.teleportTo"
            :display-directive="options.displayDirective" :hide-overlay="options.hideOverlay"
            :overlay-transition="options.overlayTransition" :content-transition="options.contentTransition"
            :click-to-close="options.clickToClose" :esc-to-close="options.escToClose" :background="options.background"
            :lock-scroll="options.lockScroll" :reserve-scroll-bar-gap="options.reserveScrollBarGap"
            :swipe-to-close="options.swipeToClose" class="modal-body"
            content-class="max-w-xl mx-4 p-4 bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-lg space-y-2">
            <div class="row justify-center justify-content-end">
                <div class="col-6">
                    <h1 class="modal-title">
                        DETALLE DE RECHAZOS - {{ selectedOrderInfo.Orden }}
                    </h1>
                </div>
                <div class="d-flex col-6 justify-content-end">
                    <button id="standard-close-button" class="btn col-6 justify-content-end"
                        v-on:click="options.modelValue = false; cleanDetailVariables()">
                        <img id="standard-close-button-img" src="/arrow_back.svg">
                    </button>
                </div>
            </div>
            <div class="row" id="dashboard-graph-table-modal">
                <table class="table table-hover align-middle">
                    <thead class="dataset-headers align-middle">
                        <tr>
                            <th scope="col">ZFER</th>
                            <th scope="col">Descripción</th>
                            <th scope="col">Pieza</th>
                            <th scope="col">Cliente</th>
                            <th scope="col">Mercado</th>
                            <th scope="col">Nivel</th>
                            <th scope="col">Formula</th>
                            <th scope="col">Puesto</th>
                            <th scope="col">Clave</th>
                            <th scope="col">Horas</th>
                            <th scope="col">Plan</th>
                            <th scope="col">Real</th>
                            <th scope="col">Sobrecosto</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="dataset-entry">{{ selectedOrderInfo.ZFER }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Vehiculo }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.CodTipoPieza }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Cliente }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Mercado }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Nivel }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Formula }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.Puestodetrabajo }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.KeyModel }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.HorasQuietas }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.CostoPlan }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.CostoReal }}</td>
                            <td class="dataset-entry">{{ selectedOrderInfo.RelacionSobrecosto }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <template v-if="typeof orderDetailsDefect === 'object' && typeof orderDetailsOrigin === 'object'">
                <div class="row">
                    <div class="col col-6 modal-chart-canvas">
                        <LineBarChart :xdata="orderDetailsDefect.Defecto" :ydataBar="orderDetailsDefect.Cantidad"
                            :ydataLine="orderDetailsDefect.Porcentaje" :chartTitle="'Rechazos agrupados por defecto'"
                            class="modal-chart" />
                    </div>
                    <div class="col col-6 modal-chart-canvas">
                        <LineBarChart :xdata="orderDetailsOrigin.Origen" :ydataBar="orderDetailsOrigin.Cantidad"
                            :ydataLine="orderDetailsOrigin.Porcentaje" :chartTitle="'Rechazos agrupados por origen'"
                            class="modal-chart" />
                    </div>
                </div>
            </template>
        </VueFinalModal>
        <ModalsContainer />
    </div>
</template>

<style>
option {
    font-size: 0.85rem;
}

th {
    background-color: #B8D3D8 !important;
}

table {
    border-style: solid;
    border-color: #22222234 !important;
    border-width: 0.1rem;
    border-spacing: 0;
    border-radius: 0.7rem;
    border-collapse: collapse;
    margin-left: 0.8rem;
    overflow: hidden;
    padding: 0 !important;
}

.clean-filter-icon {
    margin-bottom: 0.5rem;
    margin-top: 0.3rem;
    margin-left: 0.3rem;
    width: 1.1rem;
}

.clean-filter-icon:hover {
    filter: invert(1)
}

.context-button {
    margin-top: 0.4rem;
    margin-bottom: 0.3rem;
    padding: 0.35rem 0.4rem;
    vertical-align: bottom;
    width: 100%;
}

.context-button-icon {
    filter: invert(1);
    margin-right: 0.6rem;
    padding: 0;
    width: 1.1rem;
}

.dashboard-filter-label {
    font-weight: bold;
    margin-top: 0.6rem;
}

.dashboard-filter-radio {
    margin-left: 0.2rem;
    width: 10%;
}

.dashboard-radio-filter-body {
    background-color: white;
    border-radius: 0.7rem;
    margin-bottom: 0.2rem;
    margin-top: 0.3rem;
}

.dashboard-filter-radio-label {
    margin-top: auto;
    margin-bottom: auto;
    width: 80%;
    font-size: 0.85rem;
    margin-left: 0.3rem;
}

.dashboard-filter-search {
    border-radius: 0.4rem;
    border-style: none;
    font-size: 0.9rem;
    padding: 0.2rem 0.3rem;
    width: 100%;
}

.dashboard-filter-select {
    background-color: white;
    border-color: rgb(219, 219, 219);
    border-radius: 0.4rem;
    margin-top: 0.2rem;
    margin-bottom: 0.2rem;
    min-height: 8rem;
    padding-left: 0.1rem;
    width: 100%;
}

.dataset-entry {
    background-color: transparent !important;
    font-size: 0.75rem !important;
    text-align: center;
    max-width: 100px;
    padding-left: 0.2rem !important;
    padding-right: 0.2rem !important;
}

.dataset-headers {
    font-size: 0.9rem;
    position: sticky;
    top: 0;
    text-align: center;
}

.table-filter-header {
    color: #222222;
    text-decoration: none;
}

.active-sort-ASCENDING::before {
    content: '▲ ';
}

.active-sort-DESCENDING::before {
    content: '▼ ';
}

.measure {
    min-width: 7rem;
    margin-top: 0.8rem;
    margin-left: 0.8rem;
    margin-bottom: 0.2rem;
    margin-right: 0.4rem;
    padding: 0;
    border-color: #22222234;
    border-radius: 0.4rem;
    border-style: solid;
    border-width: 0.1rem;
    overflow: hidden;
}

.measure-header {
    background-color: #B8D3D8;
    font-weight: bold;
    line-height: 2.5rem;
    height: 2.8rem;
    text-align: center;
}

.measure-header-title {
    font-size: 0.9rem !important;
    margin: 0;
    display: inline-block;
    line-height: 1.4;
    vertical-align: middle;
}

.measure-body {
    align-items: center;
    background-color: white;
    height: 2.5rem;
    line-height: 2.5rem;
    text-align: center;
}

.measure-body-content {
    font-size: 1.1rem !important;
    margin: 0;
}

.modal-chart {
    border-style: solid;
    border-color: #22222234;
    border-radius: 0.8rem;
    border-width: 0.1rem;
    margin: 0.4rem auto;
    max-width: 85%;
}

.modal-chart-canvas {
    padding: 0;
}

.clear-background {
    background-color: transparent;
}

.green-background {
    background-color: #b6e7b6;
}

.yellow-background {
    background-color: #FFF7AB;
}

.red-background {
    background-color: #FFABAB;
}

#dashboard-body {
    min-height: 100vh;
}

#dashboard-filter-column {
    background-color: #B8D3D8;
    overflow: auto;
    padding-left: 1.3rem;
    padding-right: 1.3rem;
}

#dashboard-graph-table {
    margin: auto;
    margin-top: 0.8rem;
    max-height: 250vh;
    overflow-x: auto;
    overflow-y: auto;
    padding-right: 1.4rem;
}

#dashboard-graph-table-modal {
    margin: auto;
    margin-top: 0.8rem;
    margin-bottom: 1rem;
    max-height: 200vh;
    overflow-x: hidden;
    overflow-y: hidden;
    padding-right: 1.5rem;
}

#dashboard-filter-complex-body {
    margin-top: 0.4rem;
    margin-bottom: 1.2rem;
}

#dashboard-graph-measures {
    top: 5rem;
    background-color: #FAFAFA;
    border-color: #22222234;
    border-radius: 0.8rem;
    border-style: none none solid none;
    border-width: 0.1rem;
    margin-bottom: 0.3rem;
    padding-bottom: 0.5rem;
    position: sticky;
    z-index: 3;
}

#details-icon {
    width: 2rem;
}
</style>