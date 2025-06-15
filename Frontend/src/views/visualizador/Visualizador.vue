<script setup>
import * as yup from 'yup';
import { ref, onMounted, watch } from 'vue';
import { ModalsContainer, VueFinalModal } from 'vue-final-modal';
import { Field, Form, ErrorMessage } from 'vee-validate';
import {
    actualizarPlanos, cargarInfoOrden,
    cargarPlanoOrden, cargarCaracteristicasOrden,
    actualizarLecciones, cargarLeccionesAprendidas,
    sortData, asignarImagenALeccion, differentials_map
} from '../visualizador/functions'
import { loadReport, populateProblemTypes } from './reportFormFunctions.js'

// Definir props
const props = defineProps({
    preloadOrder: {
        type: Number,
        required: false
    }
})

// Definir variables de la operación
const charsOrden = ref(null);
const commonChars = ref(null);
const differentials = ref(null);
const errorMessage = ref(null);
const leccionesCargadas = ref(null);
const infoOrden = ref(null);
const ordenProduccion = ref(null);
const planoOrden = ref(null);
const placeHolderOrden = ref("Ingrese una orden de producción")
const imagenLeccionActual = ref(null);
const urlVideoLeccionActual = ref(null);
const cargaFinalizada = ref(true)

const listaPuestosTrabajo = ref([
    { text: 'Corte', value: '01CORTE' },
    { text: 'Mecanizado', value: '02CNC' },
    { text: 'Serigrafía', value: '03SERIG' },
    { text: 'Vitrificado', value: '04SER_VT' },
    { text: 'Empalme', value: '05EMPAL' },
    { text: 'Curvado', value: '06CURVAD' },
    { text: 'Recorte', value: '07RECORT' },
    { text: 'Pulido', value: '08PULIDO' },
    { text: 'Serigrafía ruco', value: '08S_RUCO' },
    { text: 'Templado químico', value: '09IOX' },
    { text: 'Zund', value: '11ZUND' },
    { text: 'Preensamble', value: '12P_ENSA' },
    { text: 'Ensamble', value: '14ENSAM' },
    { text: 'Embolsado', value: '15EMBOL' },
    { text: 'Autoclave', value: '16ACV' },
    { text: 'Encapsulado', value: '17ENCAP' },
    { text: 'Inspección final', value: '18INSFIN' },
]);
const puestoActual = ref(null);

// Definir variables modificadas
const groupedChars = ref({});

// Definir funciones para variables
async function filterDiferenciales() {
    commonChars.value = null
    differentials.value = null
    charsOrden.value = await cargarCaracteristicasOrden(ordenProduccion.value)
    let commonData = Object.fromEntries(
        Object.entries(charsOrden.value)
            .filter(([key, value]) => key === "Area" || key === "Nivel")
    );
    let diffData = Object.fromEntries(
        Object.entries(charsOrden.value)
            .filter(([key, value]) => key !== "Area" && key !== "Nivel" && key !== "ZFER")
    );
    commonChars.value = commonData
    differentials.value = diffData
}

function agruparDiferenciales() {
    for (const item of leccionesCargadas.value) {
        if (!groupedChars.value[differentials_map[item.Diferencial]]) {
            groupedChars.value[differentials_map[item.Diferencial]] = [];
        }
        groupedChars.value[differentials_map[item.Diferencial]].push(item)
    }
    groupedChars.value = sortData(groupedChars.value)

}

async function cargarLecciones() {
    leccionesCargadas.value = await cargarLeccionesAprendidas(infoOrden.value[0].PuestodeTrabajo, differentials.value, infoOrden.value[0].ZFER) // Cargar las lecciones aprendidas
    leccionesCargadas.value = asignarImagenALeccion(leccionesCargadas.value)
    agruparDiferenciales() // Agrupa todas las lecciones aprendidas por diferencial para anidarlas en una tabla
}

async function cargarOrden() {
    if (ordenProduccion.value > 10000000 && ordenProduccion.value < 9999999999) {
        // Resetear todas las variables
        cargaFinalizada.value = false
        await actualizarLecciones()
        charsOrden.value = null
        errorMessage.value = null
        placeHolderOrden.value = null
        leccionesCargadas.value = null;
        groupedChars.value = {};

        //Llamado de funciones
        planoOrden.value = URL.createObjectURL(await cargarPlanoOrden(ordenProduccion.value))
        infoOrden.value = await cargarInfoOrden(ordenProduccion.value)
        if (infoOrden.value) {
            await filterDiferenciales() // Separa los diferenciales y las características comunes de una orden
            puestoActual.value = infoOrden.value[0].PuestodeTrabajo
            planoOrden.value = URL.createObjectURL(await cargarPlanoOrden(ordenProduccion.value))
            placeHolderOrden.value = ordenProduccion.value
            ordenProduccion.value = null
            cargaFinalizada.value = true
        }
        else {
            planoOrden.value = null
            infoOrden.value = null
            errorMessage.value = 'Esta orden de producción no esta activa o no existe en el sistema'
            ordenProduccion.value = null
            placeHolderOrden.value = "Ingrese una orden de producción"
            cargaFinalizada.value = true

        }
    }
}

function valoresLeccionActual(leccion) {
    imagenLeccionActual.value = leccion.Imagen
    urlVideoLeccionActual.value = leccion.URLVideo
}

// Definir ejecuciones temporales
onMounted(async () => {
    //await actualizarPlanos()
    if (props.preloadOrder) {
        ordenProduccion.value = props.preloadOrder
    }
})

// Construir modal para detalle de lecciones aprendidas
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

function reset() {
    options.value = getInitialValues()
}

// Variables para formulario de reporte de problemas
const tiposDisponibles = ref([]);
const areasDisponibles = ref([
    { text: 'Fullkit', value: 'Fullkit' },
    { text: 'Producto', value: 'Producto' },
    { text: 'Lecciones aprendidas', value: 'LeccionesAprendidas' }
])
const areaSeleccionada = ref("");
const tipoSeleccionado = ref("");
const cedulaReporte = ref("");
const descripcionProblema = ref("");

// Esquema para validación de errores
const schema = yup.object({
    'reporte-problemas-cedula': yup.number().required().label('Cédula'),
    'reporte-problemas-descripcion': yup.string().required().label('Descripción'),
    'reporte-problemas-tipo': yup.string().required(),
    'reporte-problemas-area': yup.string().required()
})

// Actualizar los tipos disponibles dependiendo de la categoría seleccionada
watch(areaSeleccionada, (categoria) => {
    tipoSeleccionado.value = ""
    tiposDisponibles.value = populateProblemTypes(categoria)
})

watch(ordenProduccion, async (orden) => {
    await cargarOrden()
})

//Actualizar las lecciones aprendidas si cambia el puesto de trabajo
watch(puestoActual, (puesto) => {
    infoOrden.value[0].PuestodeTrabajo = puesto
    leccionesCargadas.value = null;
    groupedChars.value = {};

    cargarLecciones()
})

function resetForm() {
    areaSeleccionada.value = "";
    tipoSeleccionado.value = "";
    cedulaReporte.value = "";
    descripcionProblema.value = "";
}

async function encolarReporte() {
    let body = {
        "Cedula": cedulaReporte.value,
        "Categoria": areaSeleccionada.value,
        "Tipo": tipoSeleccionado.value,
        "Descripcion": descripcionProblema.value,
        "PuestoTrabajo": infoOrden.value[0].PuestodeTrabajo,
        "Orden": placeHolderOrden.value
    }
    await loadReport(body)
    reset()
    resetForm()
}

</script>

<template>
    <p id="app-title">LECCIONES APRENDIDAS DE ORDENES DE PRODUCCIÓN</p>
    <!-- Loading animation -->
    <div class="fullpage-loading-screen" v-if="!cargaFinalizada">
        <VueSpinnerOval class="loading-screen-ovalspinner" size="60" color="#5F7A83"></VueSpinnerOval>
    </div>

    <!-- Interface -->
    <div class="row viewer-body flex-grow-1" ref="interfaceImageContainer">
        <div class="col-12 col-xl-7 viewer-interface">
            <h2 class="input-field-header">Orden
                <input class="input-field" name="input-field" v-model="ordenProduccion" :placeholder="placeHolderOrden" type="number"
                    autofocus="autofocus">
            </h2>

            <template v-if="infoOrden && cargaFinalizada">
                <div class="row viewer-interface-canvas">
                    <a :href="planoOrden" target="_blank" class="plano-orden-produccion-a">
                        <img :src="planoOrden" id="plano-orden-produccion" alt="Plano de la orden introducida" />
                    </a>
                </div>
                <div class="row viewer-order-data table-responsive" ref="interfaceDataContainer">
                    <table class="datatable table table-hover align-middle text-center">
                        <caption class="table-caption">
                            Información de la pieza
                        </caption>
                        <thead class="visualizador-table-header table-light">
                            <tr class="table-caption">
                                <th scope="col">ZFER</th>
                                <th scope="col">Vehiculo</th>
                                <th scope="col">Pieza</th>
                                <th scope="col">Cliente</th>
                                <th scope="col">Geometría</th>
                                <th scope="col">Mercado</th>
                                <th scope="col">Nivel</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th scope="row">{{ infoOrden[0].ZFER }}</th>
                                <td>{{ infoOrden[0].Vehiculo }}</td>
                                <td>{{ infoOrden[0].CodTipoPieza }}</td>
                                <td>{{ infoOrden[0].Cliente }}</td>
                                <td>{{ infoOrden[0].Geometria }}</td>
                                <td>{{ infoOrden[0].Mercado }}</td>
                                <td>{{ commonChars.Nivel }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="row viewer-differentials table-responsive" ref="interfaceDataContainer">
                    <table class="datatable table table-hover align-middle">
                        <caption class="table-caption">
                            Diferenciales
                        </caption>
                        <tbody class="text-left">
                            <tr>
                                <td>
                                    <ul class="differentials-list">
                                        <li class="differentials-list-item" v-for="(item, index) in differentials">
                                            {{ index }}
                                        </li>
                                    </ul>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </template>
            <template v-else-if="!infoOrden && cargaFinalizada">
                <h4 id="error-message" title="Error: Orden de producción no encontrada">{{ errorMessage }}</h4>
            </template>
        </div>

        <template v-if="planoOrden && infoOrden && commonChars && cargaFinalizada">
            <div class="col-12 col-xl-5 viewer-interface-lessons" ref="interfaceLectionsContainer">
                <div class="problem-publish-section">
                    <button type="button" class="btn btn-danger" id="problem-publish-button"
                        @click="options.modelReportValue = true">REPORTAR PROBLEMA</button>
                </div>
                <div class="row viewer-order-data table-responsive" id="visualizador-tabla-lecciones"
                    ref="interfaceDataContainer">
                    <table class="datatable table table-hover table-striped align-middle">
                        <caption class="table-caption">
                            Lecciones aprendidas para el puesto de trabajo:
                            <span>
                                <Field v-model="puestoActual" title="Selección del puesto de la lección aprendida"
                                    name="lecciones-aprendidas-puesto" id="lecciones-aprendidas-puesto"
                                    as="select">
                                    <option disabled value="">Seleccione una opción</option>
                                    <option v-for="puesto in listaPuestosTrabajo" :value="puesto.value">
                                        {{ puesto.text }}
                                    </option>
                                </Field>
                            </span>
                        </caption>
                        <thead class="text-center table-light">
                            <tr>
                                <th scope="col">Diferencial</th>
                                <th scope="col">Lecciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(group, diferencial) in groupedChars" :key="diferencial">
                                <th class="text-center">
                                    {{ (typeof diferencial === 'undefined') ? "" : diferencial }}
                                </th>
                                <td class="text-left">
                                    <ul class="lista-lecciones">
                                        <li class="lista-lecciones-item" v-for="item in group" :key="item.ID">
                                            <a v-if="item.Imagen || item.URLVideo" href="#"
                                                @click="valoresLeccionActual(item); options.modelValue = true">
                                                {{ item.Lecciones }}
                                            </a>
                                            <p v-else>{{ item.Lecciones }}</p>
                                        </li>
                                    </ul>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </template>
    </div>

    <!-- Modal lecciones aprendidas -->
    <div class="flex modal-background" v-if="options.modelValue">
        <VueFinalModal v-model="options.modelValue" :teleport-to="options.teleportTo"
            :display-directive="options.displayDirective" :hide-overlay="options.hideOverlay"
            :overlay-transition="options.overlayTransition" :content-transition="options.contentTransition"
            :click-to-close="options.clickToClose" :esc-to-close="options.escToClose" :background="options.background"
            :lock-scroll="options.lockScroll" :reserve-scroll-bar-gap="options.reserveScrollBarGap"
            :swipe-to-close="options.swipeToClose" class="modal-lecciones"
            content-class="max-w-xl mx-4 p-4 bg-white dark:bg-gray-900 border dark:border-gray-700 rounded-lg space-y-2">
            <div class="row justify-center justify-content-end">
                <div class="col-6">
                    <h1 class="ext-xl">
                        Detalle
                    </h1>
                </div>
                <div class="d-flex col-6 justify-content-end">
                    <button id="standard-close-button" class="btn col-6 justify-content-end"
                        @click="options.modelValue = false">
                        <img id="standard-close-button-img" src="/arrow_back.svg">
                    </button>
                </div>
            </div>
            <div class="row modal-leccion">
                <div class="col-6 modal-leccion-imagen justify-content-center">
                    <a :href="imagenLeccionActual" target="_blank"><img id="imagenLeccion" class=""
                            :src="imagenLeccionActual" v-if="imagenLeccionActual">
                    </a>
                </div>
                <div class="col-6 modal-leccion-video">
                    <iframe id="embeded-video" :src="urlVideoLeccionActual.replace('watch?v=', 'embed/')"
                        title="YouTube video player" frameborder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
                    </iframe>
                </div>
            </div>
        </VueFinalModal>
        <ModalsContainer />
    </div>

    <!-- Modal reportar alertas -->
    <div class="flex modal-background" v-if="options.modelReportValue">
        <VueFinalModal v-model="options.modelReportValue" :teleport-to="options.teleportTo"
            :display-directive="options.displayDirective" :hide-overlay="options.hideOverlay"
            :overlay-transition="options.overlayTransition" :content-transition="options.contentTransition"
            :click-to-close="options.clickToClose" :esc-to-close="options.escToClose" :background="options.background"
            :lock-scroll="options.lockScroll" :reserve-scroll-bar-gap="options.reserveScrollBarGap"
            :swipe-to-close="options.swipeToClose" class="modal-forms">

            <div class="row justify-center justify-content-end">
                <div class="col-10">
                    <h3 class="form-header">
                        Reportar un problema
                    </h3>
                </div>
                <div class="d-flex col-2 justify-content-end">
                    <button id="standard-close-button" class="btn col-6 justify-content-end" @click="options.modelReportValue = false; areaSeleccionada = '';
                    tipoSeleccionado = '', descripcionProblema = '', cedulaReporte = ''">
                        <img id="standard-close-button-img" src="/arrow_back.svg">
                    </button>
                </div>
            </div>
            <div class="row">
                <p class="form-caption">Con este formulario puede alertar de un problema en la orden de producción
                    escaneada
                </p>
            </div>
            <div class="row">
                <Form class="col reporte-problemas-form" :validation-schema="schema" @submit="encolarReporte">
                    <div class="reporte-problemas-form-body">
                        <label for="reporte-problemas-cedula" class="reporte-problemas-form-label"> Cédula
                        </label>
                        <Field v-model="cedulaReporte" title="Campo de cédula" name="reporte-problemas-cedula"
                            id="reporte-problemas-cedula" class="reporte-problemas-form-field"
                            placeholder="Escriba su cédula aquí" as="input">
                        </Field>
                        <ErrorMessage name="reporte-problemas-cedula" v-slot="{ message }">
                            <p class="error-message">Este campo es obligatorio y solo debe contener números</p>
                        </ErrorMessage>
                    </div>

                    <div class="reporte-problemas-form-body">
                        <label for="reporte-problemas-area" class="reporte-problemas-form-label"> Categoría </label>
                        <Field v-model="areaSeleccionada" title="Selección de categoría del problema"
                            name="reporte-problemas-area" id="reporte-problemas-area"
                            class="reporte-problemas-form-field" as="select">
                            <option disabled value="">Seleccione una opción</option>
                            <option v-for="area in areasDisponibles" :value="area.value">
                                {{ area.text }}
                            </option>
                        </Field>
                        <ErrorMessage name="reporte-problemas-area" v-slot="{ message }" class="error-message">
                            <p class="error-message">Este campo es obligatorio</p>
                        </ErrorMessage>
                    </div>

                    <div class="reporte-problemas-form-body" v-if="areaSeleccionada !== ''">
                        <label for="reporte-problemas-tipo" class="reporte-problemas-form-label"> Tipo de problema
                        </label>
                        <Field v-model="tipoSeleccionado" title="Selección de tipo de problema"
                            name="reporte-problemas-tipo" id="reporte-problemas-tipo"
                            class="reporte-problemas-form-field" as="select">
                            <option disabled value="">Seleccione una opción</option>
                            <option v-for="tipo in tiposDisponibles" :value="tipo">
                                {{ tipo }}
                            </option>
                        </Field>
                        <ErrorMessage name="reporte-problemas-tipo" v-slot="{ message }" class="error-message">
                            <p class="error-message">Este campo es obligatorio</p>
                        </ErrorMessage>
                    </div>

                    <div class="reporte-problemas-form-body" v-if="tipoSeleccionado !== ''">
                        <label for="reporte-problemas-descripcion" class="reporte-problemas-form-label"> Descripción
                        </label>
                        <Field v-model.lazy="descripcionProblema" title="Campo de descripción del problema"
                            name="reporte-problemas-descripcion" id="reporte-problemas-descripcion"
                            class="reporte-problemas-form-field" placeholder="Escriba aquí su problema" as="textarea">
                        </Field>
                        <ErrorMessage name="reporte-problemas-descripcion" v-slot="{ message }" class="error-message">
                            <p class="error-message">Este campo es obligatorio</p>
                        </ErrorMessage>
                    </div>

                    <div class="reporte-problemas-form-body d-flex justify-content-center"
                        v-if="descripcionProblema !== ''">
                        <button class="reporte-problemas-send-button">Enviar</button>
                    </div>
                </Form>
            </div>
        </VueFinalModal>
        <ModalsContainer />
    </div>

    <div class="chatbot-icon-container">
        <a href="https://chat.openai.com/" target="_blank" class="">
            <img src="/chatbot_icon.svg" id="chatbot-icon" alt="Icono de apertura de chatbot">
        </a>
    </div>
</template>

<style>
/* Sección de estilos para los componentes del visualizador */
.datatable {
    width: 100% !important;
}

li,
td,
tr,
th {
    font-size: 1em !important;
}

.input-field-header {
    font-size: 1.5rem;
    margin: 1rem 0rem;
    margin-bottom: 0.2rem;
    margin-left: 1rem !important;
    margin-right: 1rem !important;
    padding: 0 0.5rem !important;
}

.input-field {
    border-radius: 0.5rem;
    font-size: 16px !important;
    margin: 0;
    margin-top: 0.3rem;
    padding: 0.2rem 0.5rem;
    width: 100%;
}

.lista-lecciones {
    list-style-type: none;
    margin: 0.1rem 0;
}

.lista-lecciones-item {
    margin-bottom: 0.6rem;
    line-height: 1.5;
}

.lista-lecciones-item::marker {
    content: '⚠  ';
}

.viewer-input {
    margin: 0.6rem 0rem !important;
}

.viewer-body {
    height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

.viewer-interface {
    border-right: solid;
    border-color: #E3EAEB;
    border-width: 0.1rem;

}

.viewer-interface-canvas {
    margin-left: auto;
    margin-right: auto;
    min-width: 3rem;
}

.viewer-order-data {
    bottom: 4rem;
    margin: 1rem 1rem;
}

.vld-container {
    position: relative;
    height: 100%;
    width: 100%;
}

.plano-orden-produccion-a {
    margin: 0 !important;
    padding: 0 !important;
    text-align: center;
}

.differentials-list {
    columns: 3;
    margin: 0
}

.viewer-differentials {
    margin: 0 1rem;
    padding: 0;
}

.table-striped>tbody>tr:nth-child(2n+1)>td,
.table-striped>tbody>tr:nth-child(2n+1)>th {
    background-color: #E0F6FF !important;
}

.table-caption {
    background-color: #8fc5cf !important;
    border-color: #cdcfcf;
    border-radius: 10px 10px 0 0;
    border-style: solid;
    border-width: 0.1rem;
    caption-side: top;
    color: #222323;
    font-size: 1.1em;
    font-weight: bolder;
    text-align: center;
}

.modal-background {
    background-color: #222323;
    margin: 0 !important;
    padding: 0 !important;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    opacity: 60%;
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 100;
}

.modal-lecciones {
    top: 8rem;
    bottom: 4rem;
    max-width: 80vw;
    margin: auto;
}

.modal-leccion-imagen {
    padding: 0.5rem 1rem;
}

.modal-leccion-video {
    padding: 0.5rem 1rem;
}

.problem-publish-section {
    margin: 0.4em 1em;
    text-align: right;
}

.differentials-list-item {
    margin-left: 1em;
    margin-right: 1em;
}

.differentials-list-item::marker {
    content: "🔹  ";
}

#error-message {
    color: red;
    margin-left: 1.5rem;
    margin-top: 1rem;
}

#embeded-video {
    height: 100%;
    width: 100%;
}

#imagenLeccion {
    border: solid;
    border-color: #E3EAEB;
    border-radius: 1rem;
    max-width: 100%;
    margin: auto;
}

#plano-orden-produccion {
    margin: 1.5rem 0;
    border: solid;
    border-color: #222323;
    border-width: 0.1rem;
    max-height: 400px;
    max-width: 85%;
}

#plano-orden-produccion:hover {
    opacity: 60%;
}

#problem-publish-button {
    font-size: 1em;
    font-weight: bold;
}

#visualizador-tabla-lecciones {
    max-height: 30rem;
    overflow-x: hidden !important;
    overflow-y: auto !important;
}

/* Estilos para el formulario de reporte de problemas */
.form-header {
    align-items: center;
    color: #222323;
    display: flex;
    font-size: 1.3em;
    font-weight: bolder !important;
    height: 100%;
    margin: 0;
}

.form-caption {
    font-size: 1.1em !important;
    margin: 0.6em 0 1.3em;
}

.modal-forms {
    background-color: #fafafa;
    border-radius: 3%;
    padding: 2.5rem;
    top: 5.5rem;
    bottom: 4.5rem;
    min-width: 50vw;
    max-width: 60vw;
    margin: auto;
    overflow: auto;
}

.modal-forms-content {
    display: flex;
    flex-direction: column;

}

.reporte-problemas-form-body {
    margin: 0;
    padding: 0;
    width: 100%;
}

.reporte-problemas-form-label {
    color: #222323;
    font-weight: bold;
    margin-top: 0.6rem;
    margin-bottom: 0.4rem;
    padding: 0;
}

.reporte-problemas-form-field {
    border-color: #d1d1d1;
    border-radius: 0.3rem;
    border-width: 0.1rem;
    box-shadow: none;
    color: #222323;
    display: flex;
    height: 2.5rem;
    outline-color: #8fc5cf;
    padding: 0.2rem 0.4rem;
    width: 100%;
}

.error-message {
    color: red;
}

.reporte-problemas-send-button {
    background-color: #8fc5cf;
    border-width: 0;
    border-radius: 0.5rem;
    color: #222323;
    font-weight: bolder;
    margin-top: 1rem;
    padding: 0.3rem 1rem;
}

.reporte-problemas-send-button:hover {
    background-color: #61868d;
    color: #fafafa;
}

.reporte-problemas-send-button:active {
    background-color: #3c5257;
    color: #fafafa;
}

#reporte-problemas-descripcion {
    height: 9rem;
}

/* Estilos para ChatBot */
.chatbot-icon-container {
    margin: 1rem;
    position: fixed;
    text-align: right;
    bottom: 4em;
    right: 0rem;
    visibility: hidden;
}

#chatbot-icon {
    background-color: #fafafa;
    border-radius: 100%;
    filter: brightness(40%);
    filter: invert(0.9);
    padding: 0.8rem;
    width: 5.5rem;
}

#chatbot-icon:hover {
    background-color: white;
    filter: brightness(90%);
    filter: invert(0);
    transition-duration: 145ms;
}

</style>
