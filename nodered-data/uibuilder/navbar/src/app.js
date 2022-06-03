
import Vue from "vue";
import App from "./components/App.vue";
import router from "./router";


import moment from "moment";

moment.locale('es');


// import uibuilder from "./../../../node_modules/node-red-contrib-uibuilder/front-end/src/uibuilderfe.js";

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// import VueSmartWidget from 'vue-smart-widget'

// Vue.use(VueSmartWidget)

// import {SmartWidget} from 'vue-smart-widget'

// Vue.component('SmartWidget', SmartWidget)

// import { SmartWidgetGrid } from 'vue-smart-widget'

// Vue.component('SmartWidgetGrid', SmartWidgetGrid)

// Install BootstrapVue
Vue.use(BootstrapVue);
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin);




import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

// Optionally install the vue-json-pretty components
import VueJsonPretty from 'vue-json-pretty';
import 'vue-json-pretty/lib/styles.css';
Vue.component('VueJsonPretty', VueJsonPretty);


import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)

Vue.component('apexchart', VueApexCharts)


// import ECharts from 'vue-echarts'
// import { use } from 'echarts/core'


// Vue.component('v-chart', ECharts)


import { Plotly } from 'vue-plotly'
Vue.use(Plotly)
Vue.component('Plotly', Plotly)

window.uibuilder = uibuilder;
uibuilder.start('/navbar', '/uibuilder/vendor/socket.io')
// uibuilder.start()

// Enable Devtools
Vue.config.devtools = true

new Vue({
  el: "#app",
  // runtimerCompiler: true,
  router,
  render: (h) => h(App),
});
