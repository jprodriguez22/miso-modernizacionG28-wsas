<script setup>
import { ref, onMounted, onUpdated, watch } from 'vue';
import { RouterLink } from 'vue-router';
import { useField, useForm, useFieldArray } from 'vee-validate'

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

const listStudentErrors = ref([])

// Validation schema for form
const { handleSubmit, handleReset, errors } = useForm({
    initialValues: {
        studentIDCard: [{ value: '' }]
    },
    validationSchema: {
        teacherIDCard(value) {
            if (/^[0-9]*$/.test(value)) {
                if (value > 0) return true
                return 'El valor debe ser mayor a 0'
            }
            return 'El valor solo puede contener valores numéricos'
        },
        studentIDCard: (studentIDCards) => {
            const response = studentIDCards.map((id) => {
                const value = id.value;
                if (/^[0-9]*$/.test(value)) {
                    if (value > 0) return ''
                    return 'El valor debe ser mayor a 0'
                }
                return 'El valor solo puede contener valores numéricos'
            });
            listStudentErrors.value = response
            return response
        },
        stationSelect(value) {
            if (value) return true
            return 'Debe seleccionar un puesto de trabajo'
        },
        fileUpload(value) {
            if (value) {
                if (value.size < 5000000) return true
                return 'El archivo no puede ser superior a 5Mb'
            }
            return 'Debe cargar una evidencia al sistema'
        },
    },
})

onMounted(() => {
    id.value = props.id
})

// Constants for form
const teacherID = useField('teacherIDCard');
const stationSelect = useField('stationSelect')
const uploadedFile = useField('fileUpload')
const stations = Object.values(workStations)

const { fields: studentsID, push, remove } = useFieldArray('studentIDCard')

const submit = handleSubmit(values => {
    alert(JSON.stringify(values, null, 2))
})

function newStudent() {
    push({ value: '' })
}

function removeStudent(index) {
    remove(index)
}

</script>

<template>
    <p id="app-title">DETALLE DE NOTIFICACIÓN DE PRODUCTO</p>

    <v-row>
        <v-col cols="5">
            <v-row class="row-back-button">
                <v-col cols="1">
                    <RouterLink class="button-link" :to="{ name: 'detalleFNP', query: { id: props.id } }">
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
                    </v-card>
                </v-col>
            </v-row>
        </v-col>

        <v-col cols="7">
            <v-row class="row-trained-personal" id="trained-workers-card">
                <v-card class="card-trained-personal">
                    <v-form ref="form" validate-on="lazy" @submit.prevent="submit">
                        <v-card-text>

                            <v-row class="row-trained-personal-body" align="center">
                                <v-col cols="1">
                                    <v-icon icon="mdi-briefcase" color="primary" size="40"></v-icon>
                                </v-col>
                                <v-col>
                                    <p id="trained-workers-title">Agregar personal capacitado</p>
                                </v-col>
                            </v-row>

                            <v-divider></v-divider>

                            <v-row class="row-form-field">
                                <v-select v-model="stationSelect.value.value"
                                    :error-messages="stationSelect.errorMessage.value" :items="stations"
                                    label="Puesto de trabajo" variant="outlined" prepend-icon="mdi-layers">
                                </v-select>
                            </v-row>

                            <v-row class="row-form-field">
                                <v-text-field clearable v-model="teacherID.value.value"
                                    :error-messages="teacherID.errorMessage.value" label="Cédula entrenador"
                                    variant="outlined" prepend-icon="mdi-clipboard">
                                </v-text-field>
                            </v-row>

                            <v-row class="row-form-field">
                                <v-file-input clearable label="Evidencia capacitación"
                                    v-model="uploadedFile.value.value" show-size accept=".pdf,.docx,.doc,.xlsx,image/*"
                                    variant="outlined" :error-messages="uploadedFile.errorMessage.value"
                                    hint="Imágenes o documentos menores a 5Mb" persistent-hint>
                                </v-file-input>
                            </v-row>

                            <v-divider></v-divider>

                            <v-row class="row-form-field">
                                <v-col cols="1" id="add-student-icon-column" class="add-row-form-field"
                                    @click="newStudent">
                                    <v-icon icon="mdi-plus" size="x-large"></v-icon>
                                </v-col>
                                <v-col cols="2" class="add-row-form-field" @click="newStudent">
                                    <p id="add-row-subtitle">Agregar fila</p>
                                </v-col>
                            </v-row>

                            <v-row class="row-form-field" v-for="(student, index) in studentsID" :key="student.key"
                                align="start">
                                <v-col cols="11">
                                    <v-text-field clearable v-model="student.value.value"
                                        :error-messages="listStudentErrors[index]" label="Cédula operario"
                                        variant="outlined" hide-details="auto" type="number" prepend-icon="mdi-school">
                                    </v-text-field>
                                </v-col>
                                <v-col col="1" id="col-remove-student-icon" class="add-row-form-field">
                                    <v-icon icon="mdi-delete" @click="removeStudent(index)"></v-icon>
                                </v-col>
                            </v-row>

                        </v-card-text>
                        <v-card-actions>
                            <v-btn color="success" type="submit">Guardar</v-btn>
                            <v-btn color="error" @click="handleReset">Reiniciar</v-btn>
                        </v-card-actions>
                    </v-form>
                </v-card>
            </v-row>
        </v-col>

    </v-row>

</template>

<style>
.add-row-form-field {
    cursor: pointer;
}

.button-link {
    color: #2e2e2e;
    text-decoration: none;
}

.card-trained-personal {
    width: 100%;
}

.common-button {
    font-size: 100% !important;
}

.row-back-button {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-card-details {
    margin: 1.25rem 1.25rem;
    padding: 0.25rem;
}

.row-form-field {
    margin: 0 0.25rem;
}

.row-trained-personal {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-trained-personal-body {
    margin: 0.125rem;
}

#add-row-subtitle {
    margin: 0;
    padding: 0.125rem;
}

#add-student-icon-column {
    text-align: start;
}

#btn-return {
    border-bottom: solid;
    border-radius: 0.25rem;
    height: 3rem;
}

#col-remove-student-icon {
    margin-top: 1rem;
    text-align: center;
}

#trained-workers-title {
    font-size: 1.25rem !important;
    margin: 0 0 0 1.25rem;
    text-align: left;
}
</style>