// Importación de vistas de producción
const HomeView = () => import("../views/Home.vue");
const VisualizadorView = () => import("../views/visualizador/Visualizador.vue");
const prodDashboardCosto = () =>
  import("../views/produccion/gestionCostosPlanta/GestionCostosPlanta.vue");

// Importación de vistas de FNP
const fnpCargaCapacitacionView = () => import("./procesos/fnp/cargaCapacitacion.vue")
const fnpCreacionFormatosView = () => import("./procesos/fnp/creacionFNP.vue")
const fnplistaFormatosView = () => import("../views/procesos/fnp/listaFormatos.vue")
const fnpDetalleFormatosView = () => import("../views/procesos/fnp/detalleFormatos.vue")

import { inject } from "vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
  // Rutas generales
  { path: "/", name: "home", component: HomeView },

  // Herramientas para la gestión de la producción
  {
    path: "/produccion/leccionesaprendidas",
    name: "leccionesAprendidas",
    props: route => ({ preloadOrder: Number(route.query.order) || 0 }),
    component: VisualizadorView,
    meta: { requiresAuth: false },
  },
  {
    path: "/produccion/dashboardcosto",
    name: "dashboardCosto",
    component: prodDashboardCosto,
    meta: { requiresAuth: false },
  },

  // Herramientas para la gestión del proceso
  {
    path: "/procesos/fnp",
    name: "listaFNP",
    component: fnplistaFormatosView,
    meta: {requiresAuth: true}
  },
  {
    path: "/procesos/fnp/crear",
    name: "crearFNP",
    component: fnpCreacionFormatosView,
    meta: {requiresAuth: true}
  },
  {
    path: "/procesos/fnp/detalle/carga",
    name: "capacitarPersonal",
    component: fnpCargaCapacitacionView,
    props: route => ({ id: Number(route.query.id )}),
    meta: {requiresAuth: true}
  },
  {
    path: "/procesos/fnp/detalle",
    name: "detalleFNP",
    component: fnpDetalleFormatosView,
    props: route => ({ id: Number(route.query.id) }),
    meta: {requiresAuth: true}
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
