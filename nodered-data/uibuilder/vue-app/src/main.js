import App from './components/App.vue'
import Vue from 'vue'
import router from './router'


import moment from "moment";

moment.locale('es');

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import VueSmartWidget from 'vue-smart-widget'

Vue.use(VueSmartWidget)

import {SmartWidget} from 'vue-smart-widget'

Vue.component('SmartWidget', SmartWidget)

import { SmartWidgetGrid } from 'vue-smart-widget'

Vue.component('SmartWidgetGrid', SmartWidgetGrid)

// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)

import VueSvgGauge from 'vue-svg-gauge'
Vue.use(VueSvgGauge)


// import { Plotly } from 'vue-plotly'
// Vue.use(Plotly)
// Vue.component('Plotly', Plotly)


import VCharts from 'v-charts'
Vue.use(VCharts)



import uibuilder from 'node-red-contrib-uibuilder/front-end/src/uibuilderfe.js'
uibuilder.start('/vue-app');


// Enable Devtools
Vue.config.devtools = true

new Vue({
  el: "#app",
  // runtimerCompiler: true,
  router,
  render: (h) => h(App),
});