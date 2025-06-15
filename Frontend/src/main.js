import { createApp } from 'vue'
import App from './App.vue'

// Framework
import { createVuetify } from 'vuetify/lib/framework.mjs';
import 'vuetify/styles';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'


// Data visualization
import VueApexCharts from 'vue3-apexcharts';
import { VueSpinnersPlugin } from 'vue3-spinners'
import { createVfm } from 'vue-final-modal';

import router from './views'

import './assets/main.css'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'vue-final-modal/style.css'

const vuetify = createVuetify({
    components,
    directives,
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {
            mdi,
        }
    },
    theme: {
        defaultTheme: 'light',
        themes: {
            light: {
                colors: {
                    primary: "#b8d3d8",
                    secondary: "#2E2E2E",
                    accent: "#5f7a83",
                    error: "#DF4848",
                    info: "#2681C9",
                    success: "#239027",
                    warning: "#E58204"
                }
            }
        }
    }
});

const app = createApp(App)

const vfm = createVfm()

app.use(vuetify)
app.use(router)
app.use(VueApexCharts)
app.use(VueSpinnersPlugin)
app.use(vfm)

app.mount("#app")