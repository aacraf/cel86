<template>
  <b-container fluid class="pr-5">
    <!-- <h2 class="ml-4 mt-4">Home</h2> -->
    <b-sidebar id="sidebar-1" shadow z-index="50" no-header @shown="reduceGrid" @hidden="expandGrid">
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab">
            <b-button-group>
              <b-button block v-b-toggle.accordion-1 :disabled="add_widget_step == 0 ? false : true" variant="light">
                {{ this.add_widget_step > 0 ? this.new_widget.SignalID : 'Señales' }}</b-button>
              <b-button variant="light" v-if="this.add_widget_step > 0"
                v-on:click="() => { this.new_widget = {}; this.add_widget_step = 0; }">
                <b-icon-x-square size="1x"></b-icon-x-square>
              </b-button>
            </b-button-group>
          </b-card-header>
          <b-collapse id="accordion-1" visible accordion="my-accordion" role="tabpanel"
            :visible="add_widget_step == 0 ? true : false">
            <b-card-body>
              <!-- <b-form-input :id="`type-search`" :type="type" placeholder="buscar"></b-form-input> -->
              <b-list-group flush>
                <b-list-group-item button class="d-flex justify-content-between align-items-center py-1" variant="light"
                  v-on:click="addWidget(index, $event)" v-for="(signal,index) in Signals">
                   {{index}} <b-icon v-if="signal>0" icon="exclamation-circle-fill" variant="danger"></b-icon>
                   <!-- <b-badge variant="primary" pill>0</b-badge> -->
                </b-list-group-item>
              </b-list-group>
            </b-card-body>
          </b-collapse>
        </b-card>

        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab">
            <b-button-group>
              <b-button block v-b-toggle.accordion-2 :disabled="add_widget_step == 1 ? false : true" variant="light"> {{
                  this.add_widget_step > 1 ? this.new_widget.type : 'Widgets'
              }}</b-button>
              <b-button variant="light" v-if="this.add_widget_step > 1"
                v-on:click="() => { this.new_widget = { SignalID: this.new_widget.SignalID }; this.add_widget_step = 1; }">
                <b-icon-x-square size="1x"></b-icon-x-square>
              </b-button>
            </b-button-group>
          </b-card-header>
          <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel"
            :visible="add_widget_step == 1 ? true : false">
            <b-card-body>
              <b-row>
                <b-col>
                  <!-- <b-icon-graph-up v-on:click="addWidget('PlotlyGrafica', $event)" scale="3"></b-icon-graph-up> -->
                  <b-img v-b-tooltip.hover title="Plotly Grafica" v-on:click="addWidget('PlotlyGrafica', $event)"
                    thumbnail fluid src="https://img.icons8.com/dusk/64/undefined/line-chart.png" alt="Line Chart">
                  </b-img>
                </b-col>
                <b-col>
                  <!-- <b-icon-speedometer2 v-on:click="addWidget('Medidor', $event)" scale="3"></b-icon-speedometer2> -->
                  <b-img v-b-tooltip.hover title="Medidor" v-on:click="addWidget('Medidor', $event)" thumbnail fluid
                    src="https://img.icons8.com/external-vitaliy-gorbachev-lineal-color-vitaly-gorbachev/60/undefined/external-gauge-infographic-elements-vitaliy-gorbachev-lineal-color-vitaly-gorbachev.png"
                    alt="Gauge"></b-img>
                </b-col>
                <b-col>
                  <b-img v-b-tooltip.hover title="Apex Grafica" v-on:click="addWidget('ApexGrafica', $event)" thumbnail
                    fluid src="https://img.icons8.com/cute-clipart/64/undefined/squiggly-line.png" alt="Live Chart">
                  </b-img>
                </b-col>
              </b-row>
              <b-row>
                <b-col>
                  <!-- <b-icon-graph-up v-on:click="addWidget('PlotlyGrafica', $event)" scale="3"></b-icon-graph-up> -->
                  <b-img v-b-tooltip.hover title="Echarts Grafica" v-on:click="addWidget('EchartsGrafica', $event)"
                    thumbnail fluid
                    src="https://img.icons8.com/external-flaticons-lineal-color-flat-icons/64/undefined/external-line-chart-infographic-flaticons-lineal-color-flat-icons-19.png"
                    alt="Echarts">
                  </b-img>
                </b-col>
              </b-row>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" role="tab">
            <b-button-group>
              <b-button block v-b-toggle.accordion-3 :disabled="this.add_widget_step ? false : true" variant="light">
                Parametros</b-button>
              <b-button variant="light" v-if="this.add_widget_step > 2"
                v-on:click="() => { this.new_widget = { SignalID: this.new_widget.SignalID, type: this.new_widget.type }; this.add_widget_step = 2; }">
                <b-icon-x-square size="1x"></b-icon-x-square>
              </b-button>
            </b-button-group>
          </b-card-header>
          <b-collapse id="accordion-3" accordion="my-accordion" role="tabpanel"
            :visible="add_widget_step == 2 ? true : false">
            <b-card-body>
              <b-form-group v-if="this.new_widget.type == 'PlotlyGrafica' || this.new_widget.type == 'EchartsGrafica'" id="timesteps"
                description="h = horas, m = minutos, s = segundos" label="Ventana de tiempo" label-for="timesteps">
                <!--                 
                :invalid-feedback="invalidFeedback"
                :state="state" -->
                <b-form-input id="timesteps" v-model="timesteps" placeholder="2h"></b-form-input>
              </b-form-group>
                <!-- <b-form-checkbox v-if="this.new_widget.type == 'EchartsGrafica'"
                  id="checkbox-1"
                  v-model="status"
                  name="checkbox-1"
                  value="true"
                  unchecked-value="not_accepted"
                >
                  Grafica en tiempo real
                </b-form-checkbox> -->
              <!-- <b-calendar v-model="value" @context="onContext" locale="en-US"></b-calendar> -->
            </b-card-body>
          </b-collapse>
        </b-card>
          <b-card no-body class="mb-1 fixed-bottom">
            <b-card-header header-tag="header" role="tab" header-bg-variant="dark">
              <b-button block :disabled="add_widget_step > 0 ? false : true" variant="dark"
                v-on:click="() => { this.addWidget('', event, true) }">Añadir
              </b-button>
            </b-card-header>
        </b-card>
    </b-sidebar>
    <b-row>
      <b-col v-if="sidebarToggle==2" :cols="sidebarToggle" id="sidebar-wrapper" >
      </b-col>
      <b-col ref="widgets">
        <smart-widget-grid :layout="layout">
          <Widget v-for="(widget, index) in widgets" :key="widget.gridindex" :slot="widget.gridindex"
            :gridindex="widget.gridindex" :SignalID="widget.SignalID" :type="widget.type" :params="widget.params"
            :removeWidget="removeWidget" :alarm="widget.alarm"></Widget>
        </smart-widget-grid>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>


import Widget from './Widget.vue';

export default {
  name: "home",
  components: {
    Widget
  },
  data() {
    return {
      sidebarToggle: 0,
      estado: "",
      piezas_ok: 0,
      Signals: [],
      widgets: [],
      layout: [],
      add_widget_step: 0,
      new_widget: {},
      timesteps: "2h",
      gridindex: 1,
      // msg: "No Message Received from Node-Red",
    };
  },
  methods: {
    addWidget(signal, event, add) {
      if (this.add_widget_step == 0) {
        this.new_widget.SignalID = signal;
        if(this.Signals[signal] > 0){
          this.new_widget.alarm = {
            type: "danger",
            msg: "Fuera de límites de tolerancia"
          }
        }

        this.add_widget_step = 1;
      }
      else if (this.add_widget_step == 1) {
        // this.new_widget.loading = true;
        if (signal == "") {
          this.new_widget.type = "PlotlyGrafica";
        } else {
          this.new_widget.type = signal;
        }
        this.new_widget.params = {};
        this.add_widget_step = 2;
      }
      else if (this.add_widget_step == 2) {

      }

      if (add) {
        this.new_widget.params.timesteps = this.timesteps;
        this.new_widget.gridindex = this.gridindex;
        console.log("NEW_WIDGET", this.new_widget);
        this.layout.push({
          i: this.gridindex,
          x: 0,
          y: 0,
          w: 12,
          h: 10
        });
        this.gridindex++;
        this.widgets.push(this.new_widget);
        this.new_widget = {};
        this.add_widget_step = 0;
      }
    },
    // TODO: No funciona bien.
    removeWidget(index) {
      const gridindex = this.widgets.map(widget => widget.gridindex).indexOf(index);
      this.widgets.splice(gridindex, 1);
      const layoutIndex = this.widgets.map(layout => layout.i).indexOf(index);
      this.layout.splice(layoutIndex, 1);
    },
    expandGrid(){
      this.sidebarToggle = 0;
    },
    reduceGrid(){
      this.sidebarToggle = 2;
    },
  },
  mounted() {
    const fluxQuery = `
      from(bucket: "cel86")
        |> range(start: -15m)
        |> filter(fn: (r) => r["_measurement"] == "sensores")
        |> filter(fn: (r) => r["molde"] == "MT201")
        |> filter(fn: (r) => r._field == "value" or r._field == "value_max" or r._field == "value_min")
        |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> map(fn: (r) => ({r with _value: r.value > r.value_max or r.value < r.value_min}))
        |> filter(fn: (r) => r._value == true, onEmpty: "keep") 
        |> count(column: "_value")
        |> pivot(rowKey:["_measurement"], columnKey: ["medicion"], valueColumn: "_value")
        |> drop(columns: ["_start", "_stop", "_measurement", "molde"])
      `
    uibuilder.send({ 'topic': 'initHome', 'payload': "", 'query': fluxQuery })

    uibuilder.onChange("msg", (newMsg) => {

      if(newMsg.topic == "initHome"){
        var response = JSON.parse(newMsg.payload);
        response = response[0];
        delete response.result;
        delete response.table;
        

        this.Signals = response

      }

      this.estado = newMsg.celstate ? "EN MARCHA" : "PARADA";
      this.piezas_ok = newMsg.cel_counter_ok ? "EN MARCHA" : "PARADA";
      // if (newMsg.signal_index) {
      //   this.Signals = Object.keys(newMsg.signal_index);
      // }
    });
  },
};
</script>

<style scoped>
#toggle-sidebar {
  margin-top: 400px !important;
  height: 100px;
  /* display: none; */
}

/* #sidebar-wrapper:hover {
  background-color: green;
  height: 100%;
} */
/* 
#sidebar-wrapper:hover #toggle-sidebar {
  display: block !important;
} */


.b-list-group {
  max-height: 300px !important;
  margin-bottom: 10px !important;
  overflow: scroll !important;
  -webkit-overflow-scrolling: touch !important;
}
/deep/ .b-sidebar {
  z-index: 50;
  margin-top: 70px;
  height: 93%;
}
</style>