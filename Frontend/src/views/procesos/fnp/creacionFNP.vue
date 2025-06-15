<script setup lang="js">
import { ref, inject } from 'vue';
import { RouterLink } from 'vue-router';
import { useField, useForm, useFieldArray } from 'vee-validate'

import { cargarFNP } from './networkFunctions';

const ZFERListErrors = ref([])

const { handleSubmit, handleReset } = useForm({
    initialValues: {
        fnpZFERList: [{ value: '' }]
    },
    validationSchema: {
        fnpTitle(value) {
            if (value) return true
            return 'Este campo es obligatorio'
        },
        fnpCustomer(value) {
            if (value) return true
            return 'Este campo es obligatorio'
        },
        fnpProject(value) {
            if (value) return true
            return 'Este campo es obligatorio'
        },
        fnpZFERList: (zfers) => {
            const errors = zfers.map((zfer) => {
                const value = zfer.value;
                if (!/^\d+$/.test(value)) {
                    return 'El valor solo puede contener valores numéricos';
                }
                if (parseInt(value) <= 0) {
                    return 'El valor debe ser mayor a 0';
                }
                return ''
            });
            fnpZFERListFiltered.value = zfers.map(zfer => zfer.value);
            ZFERListErrors.value = errors.filter(e => e);      
            return errors.filter(e => e).length ? errors: true;
        }
    }
})

const fnpTitle = useField('fnpTitle')
const fnpCustomer = useField('fnpCustomer')
const fnpProject = useField('fnpProject')
const fnpZFERListFiltered = ref([])
const { fields: fnpZFERList, push, remove } = useFieldArray('fnpZFERList')

const onSubmit = handleSubmit(values => {
    cargar()
});

function newZfer() {
    push({ value: '' })
}

function removeZfer(index) {
    remove(index)
}

function cargar() {
    let body = {
        Title: fnpTitle.value.value,
        Customer: fnpCustomer.value.value,
        Project: fnpProject.value.value,
        ZFERList: fnpZFERListFiltered.value.toString(),
    }
    cargarFNP(JSON.stringify(body))
}

</script>

<template>
    <v-row>
        <v-col cols="12">
            <v-row class="row-back-button">
                <v-col cols="1">
                    <RouterLink class="button-link" :to="{ name: 'listaFNP' }">
                        <v-tab color="accent" id="btn-return">
                            VOLVER
                        </v-tab>
                    </RouterLink>
                </v-col>
            </v-row>
            <v-row class="row-form">
                <v-col cols="10" class="col-form">
                    <v-card class="card-form">
                        <v-form ref="form" validate-on="lazy" @submit.prevent="onSubmit">
                            <v-card-text class="card-body">
                                <v-row class="card-form-header" align="center">
                                    <v-col cols="1" class="card-form-header-column">
                                        <v-icon icon="mdi-plus" color="primary" size=40></v-icon>
                                    </v-col>
                                    <v-col cols="11" class="card-form-header-column">
                                        <p id="card-form-header-title">Crear nuevo formato de notificación de producto
                                        </p>
                                    </v-col>
                                </v-row>
                                <v-divider></v-divider>

                                <v-row class="card-form-body" align="center">
                                    <v-text-field clearable v-model="fnpTitle.value.value"
                                        :error-messages="fnpTitle.errorMessage.value" label="Título del formato"
                                        variant="outlined" prepend-icon="mdi-tag">
                                    </v-text-field>
                                </v-row>

                                <v-row class="card-form-body" align="center">
                                    <v-text-field clearable v-model="fnpProject.value.value"
                                        :error-messages="fnpProject.errorMessage.value" label="Nombre del proyecto"
                                        variant="outlined" prepend-icon="mdi-information">
                                    </v-text-field>
                                </v-row>

                                <v-row class="card-form-body" align="center">
                                    <v-text-field clearable v-model="fnpCustomer.value.value"
                                        :error-messages="fnpCustomer.errorMessage.value" label="Nombre del cliente"
                                        variant="outlined" prepend-icon="mdi-account">
                                    </v-text-field>
                                </v-row>

                                <v-divider></v-divider>

                                <v-row class="card-form-body">
                                    <v-col cols="1" id="add-zfer-icon-column" class="add-row-button" @click="newZfer">
                                        <v-icon icon="mdi-plus" size="x-large"></v-icon>
                                    </v-col>
                                    <v-col cols="2" @click="newZfer" class="add-row-button">
                                        <p id="add-row-subtitle">Agregar fila</p>
                                    </v-col>
                                </v-row>

                                <v-row class="card-form-body" v-for="(zfer, index) in fnpZFERList" :key="zfer.key"
                                    align="start">
                                    <v-col>
                                        <v-text-field clearable v-model="zfer.value.value"
                                            :error-messages="ZFERListErrors[index]" label="ZFER" variant="outlined"
                                            hide-details="auto" type="number" prepend-icon="mdi-information">
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="1" id="remove-zfer-icon">
                                        <v-icon icon="mdi-delete" @click="removeZfer(index)"></v-icon>
                                    </v-col>
                                </v-row>

                            </v-card-text>
                            <v-card-actions>
                                <v-btn color="success" type="submit">Guardar</v-btn>
                                <v-btn color="error" @click="handleReset">Reiniciar</v-btn>
                            </v-card-actions>
                        </v-form>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</template>

<style lang="css" scoped>
.button-link {
    color: #2e2e2e;
    text-decoration: none;
}

.card-body {
    margin: 1.25rem
}

.card-form-body {
    margin: 1rem 0.5rem;
}

.card-form-header-column {
    margin: 0.5rem auto;
    padding: auto;
    text-align: center;
}

.col-form {
    margin: auto;
    padding: auto;
}

.row-back-button {
    margin: 1.25rem;
    padding: 0.25rem;
}

.row-form {
    margin: 1.25rem;
}

.add-row-button {
    cursor: pointer;
}

#add-row-subtitle {
    margin: 0;
    text-align: start;
}

#btn-return {
    border-bottom: solid;
    border-radius: 0.25rem;
    height: 3rem;
}

#card-form-header-title {
    font-weight: bold;
    margin: 0;
}

#remove-zfer-icon {
    margin-top: 1rem;
    text-align: center;
}
</style>