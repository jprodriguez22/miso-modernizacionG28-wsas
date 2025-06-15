<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { inject, onMounted, ref, provide } from 'vue';

</script>

<template>
    <div class="container-fluid">
        <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavbar"
            aria-labelledby="offcanvasNavbarLabel">
            <div class="offcanvas-header">
                <img src="" class="logo-color" title="logo menú principal">
            </div>
            <div class="offcanvas-body">
                <div class="accordion sidebar-item-accordion" id="menuPrincipal">

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="produccionHeading">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#produccion" aria-expanded="true" aria-controls="produccion">
                                Producción
                            </button>
                        </h2>

                        <div id="produccion" class="accordion-collapse collapse" aria-labelledby="produccionHeading"
                            data-bs-parent="#menuPrincipal">

                            <div class="accordion-body">
                                <div class="accordion sidebar-item-accordion" id="cat-produccion">
                                    <h2 class="sidebar-item" id="produccion-dashboardCosto-heading">
                                        <ul class="nav flex-column nav-pills" role="tablist">
                                            <li class="sidebar-subitem" role="produccion-dashboardCosto">
                                                <router-link to="/produccion/dashboardCosto" class="sidebar-link">Costo
                                                    de ordenes de
                                                    producción</router-link>
                                            </li>
                                        </ul>
                                    </h2>
                                </div>
                            </div>

                            <div class="accordion-body">
                                <div class="accordion sidebar-item-accordion" id="cat-produccion">
                                    <h2 class="sidebar-item" id="produccion-leccionesAprendidas-heading">
                                        <ul class="nav flex-column nav-pills" role="tablist">
                                            <li class="sidebar-subitem" role="produccion-leccionesAprendidas">
                                                <router-link to="/produccion/leccionesaprendidas"
                                                    class="sidebar-link">Lecciones
                                                    Aprendidas</router-link>
                                            </li>
                                        </ul>
                                    </h2>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="accordion-item">
                        <h2 class="accordion-header" id="procesosHeading">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                data-bs-target="#procesos" aria-expanded="true" aria-controls="procesos">
                                Procesos
                            </button>
                        </h2>

                        <div id="procesos" class="accordion-collapse collapse show" aria-labelledby="procesosHeading"
                            data-bs-parent="#menuPrincipal">

                            <div class="accordion-body">
                                <div class="accordion sidebar-item-accordion" id="cat-fnp">
                                    <h2 class="sidebar-item" id="complex-capacitacionfnp-heading">
                                        <ul class="nav flex-column nav-pills" role="tablist">
                                            <li class="sidebar-subitem" role="complex-capacitacionfnp">
                                                <router-link to="/procesos/fnp" class="sidebar-link">Notificaciones de Producto</router-link>
                                            </li>
                                        </ul>
                                    </h2>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
            <div class="offcanvas-footer">
                <p id="logged-user">Bienvenido Desarrollador</p>
            </div>
        </div>
    </div>
    <router-view></router-view>
</template>

<style scoped>
.sidebar-link {
    font-size: 1rem;
    width: 100%;
}

.sidebar-item-accordion {
    margin-top: 0.2rem !important;
}
</style>
