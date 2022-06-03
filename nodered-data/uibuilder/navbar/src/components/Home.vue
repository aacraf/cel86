<template lang="html">
  <b-container fluid class="pr-5">
    <!-- <h2 class="ml-4 mt-4">Home</h2> -->
    <b-sidebar id="sidebar-1" title="Añadir" shadow>
      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" role="tab">
          <b-button block v-b-toggle.accordion-1 variant="light">Señales</b-button>
        </b-card-header>
        <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel">
          <b-card-body>
           <!-- <b-form-input :id="`type-search`" :type="type" placeholder="buscar"></b-form-input> -->
            <b-list-group flush>
              <b-list-group-item class="d-flex justify-content-between align-items-center py-1" v-for="signal in Signals">
                <span v-on:click="addGrafica(signal)">{{ signal }}</span>
                <b-badge variant="primary" pill>0</b-badge>
              </b-list-group-item>
            </b-list-group>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" role="tab">
          <b-button block v-b-toggle.accordion-2 variant="light">Widgets</b-button>
        </b-card-header>
        <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <b-row>
              <b-col>
                <b-img thumbnail fluid src="https://picsum.photos/250/250/?blur" alt="Line Chart"></b-img>
              </b-col>
              <b-col>
                <b-img thumbnail fluid src="https://picsum.photos/250/250/?blur" alt="Line Chart"></b-img>
              </b-col> 
              <b-col></b-col>
            </b-row>
          </b-card-body>
        </b-collapse>
      </b-card>

      <b-card no-body class="mb-1">
        <b-card-header header-tag="header" role="tab">
          <b-button block v-b-toggle.accordion-3 variant="light">Parametros</b-button>
        </b-card-header>
        <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel">
          <b-card-body>
            <!-- <b-calendar v-model="value" @context="onContext" locale="en-US"></b-calendar> -->
            Ventana de tiempo
            <b-form-timepicker locale="es"></b-form-timepicker>
          </b-card-body>
        </b-collapse>
      </b-card>
      </div>
    </b-sidebar>
    <b-row>
      <b-col cols="2">
        <b-button v-b-toggle.sidebar-1 variant="light" id="toggle-sidebar"><b-icon icon="chevron-bar-right"></b-icon></b-button>
      </b-col>
      <b-col ref="graficas">
      </b-col>
    </b-row>

  </b-container>
</template>

<script>
import PlotlyGrafica from './PlotlyGrafica.vue';
// import Grid from './Grid.vue'
// import Widget from './Widget.vue'
import Vue from 'vue';

export default {
  name: "home",
  components: {
    PlotlyGrafica
  },
  data() {
    return {
      estado: "",
      piezas_ok: 0,
      Signals: [],
      // msg: "No Message Received from Node-Red",
    };
  },
  methods: {
    addGrafica(signal) {
      console.log("signal", signal);
      var nuevaGrafica = Vue.extend(PlotlyGrafica)
      var instance = new nuevaGrafica({
        propsData: { SignalID: signal }
      })
      instance.$mount() // pass nothing
      this.$refs.graficas.appendChild(instance.$el)
    },
  },
  mounted() {
    uibuilder.onChange("msg", (newMsg) => {
      this.estado = newMsg.celstate ? "EN MARCHA" : "PARADA";
      this.piezas_ok = newMsg.cel_counter_ok ? "EN MARCHA" : "PARADA";
      if (newMsg.signal_index) {
        this.Signals = newMsg.signal_index;
      }
    });
  },
};
</script>

<style scoped>
.b-button #toggle-sidebar{
  margin-top: 50%
}

.b-list-group{
    max-height: 300px !important;
    margin-bottom: 10px !important;
    overflow:scroll !important;
    -webkit-overflow-scrolling: touch !important;
}
</style>