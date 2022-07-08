<template>
  <div>
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
        <b-nav-text>
          <b-button variant="dark" v-b-toggle.sidebar-1>
            <b-icon-bezier2 animation="fade" style="animation-duration: 1.75s" scale="1.0" class="text-warning">
            </b-icon-bezier2>
          </b-button>
        </b-nav-text>

        <b-nav-item to="/" exact :active="$route.name == 'home'"> <span
            class="ml-3 mr-5 mt-1 hvr-buzz-out ">CEL86</span></b-nav-item>
        <!-- <b-nav-item to="/page1" exact :active="$route.name == 'page1'">Multivariable</b-nav-item> -->
        <!-- <b-nav-item to="/page2" exact :active="$route.name == 'page2'">Modelos</b-nav-item> -->
        <!--<b-nav-item to="/page3" exact :active="$route.name == 'page3'">Info</b-nav-item>
        <b-nav-item-dropdown text="Otros" left :class="{ active: $route.path.startsWith('/page4') }">
          <b-dropdown-item to="/page4a" exact :active="$route.name == 'page4a'">Page 4a</b-dropdown-item>
          <b-dropdown-item to="/page4b" exact :active="$route.name == 'page4b'">Page 4b</b-dropdown-item>
        </b-nav-item-dropdown> -->
      </b-navbar-nav>
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item>
          <b-button v-b-modal.modal-xl variant="dark">
            <b-icon-info animation="fade" style="animation-duration: 1.75s" scale="1.5" class="text-warning mt-1">
            </b-icon-info>
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <!-- ESTADO: {{this.estado}} -->
          <b-button variant="dark">v0.1</b-button>


          <!-- v-b-tooltip.hover.left.v-danger="'Shutdown the device !'" -->
          <!-- <b-button
            size="sm"
            variant="danger"
            @click="$bvModal.show('modal-shutdown')"
            v-b-tooltip="{ trigger: 'hover', title: 'Shutdown the device', placement: 'left', variant: 'danger' }"
            ><b-icon icon="power"></b-icon
          ></b-button> -->
        </b-nav-item>
      </b-navbar-nav>
    </b-navbar>

    <!-- Shutdown Modal  -->
    <b-modal id="modal-xl" size="xl" title="Información de la aplicación">
      <div class="accordion" role="tablist">
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.usermanual variant="warning">Manual de uso</b-button>
          </b-card-header>
          <b-collapse id="usermanual" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-row>
                <b-card title="Elementos del Dashboard" :img-src="partes_app" img-alt="Elementos del Dashboard" img-top
                  tag="article" style="max-width: 20rem;" class="mb-2 ml-4">
                  <b-card-text>
                    El dashboard se puede dividir en dos partes principales: La <strong>cuadrícula</strong> de
                    visualización y la <strong>barra
                      lateral</strong> que permite añadir <em>widgets</em> a la cuadrícula. También se dispone de un
                    botón que permite
                    desplegar y esconder la barra lateral y otro que muestra un modal con información.
                  </b-card-text>
                  <!-- <b-button href="#" variant="primary">Go somewhere</b-button> -->
                </b-card>
                <b-card title="Añadir un Widget" :img-src="barra_lateral" img-alt="Añadir un Widget" img-top
                  tag="article" style="max-width: 20rem;" class="mb-2 ml-4">
                  <b-card-text>
                    Inicialmente la cuadrícula se encuentra vacía. Para añadir widgets a la cuadrícula hay que
                    recurrir a la barra lateral haciendo clic en el botón que la despliega. En la barra lateral aparecen
                    3 opciones principales donde se escogerá el <strong>sensor</strong>, el <strong>widget</strong> de
                    visualización y los <strong>parámetros</strong>.
                    Finalmente, con el botón de <strong>Añadir</strong> se añade el widget a la cuadrícula.
                  </b-card-text>
                  <!-- <b-button href="#" variant="primary">Go somewhere</b-button> -->
                </b-card>
                <b-card title="Personalziar cuadrícula" :img-src="opciones_widget" img-alt="Personalizar cuadrícula"
                  img-top tag="article" style="max-width: 20rem;" class="mb-2 ml-4">
                  <b-card-text>
                    Es posible cambiar el tamaño de los <em>widgets</em> a medida, cambiarlos de lugar o eliminarlos de
                    manera
                    que se pueda personalizar la visualización en la cuadrícula.
                    En la parte superior de cada widget, hay opciones que permiten hacer que el widget se muestre en
                    <strong>pantalla completa</strong> y también <strong>actualizar</strong>strong> el contenido de este
                    de manera que se muestre el contenido
                    como si se hubiera añadido de por primera vez.
                  </b-card-text>
                  <!-- <b-button href="#" variant="primary">Go somewhere</b-button> -->
                </b-card>
              </b-row>
              <h3 class="m-4">Widgets Disponibles</h3>
              <b-row>
                <b-card no-body class="overflow-hidden">
                  <b-row no-gutters>
                    <b-col md="4">
                      <b-card-img :src="widget_PlotlyGrafica" alt="PlotlyGrafica" class="rounded-0">
                      </b-card-img>
                    </b-col>
                    <b-col md="8">
                      <b-card-body title="PlotlyGrafica">
                        <b-card-text>
                          Este widget está basado en la librería Plotly y su enfoque es la realización de
                          análisis histórico agregando los resultados obtenidos de los modelos. En esta gráfica
                          se
                          pueden
                          observar las predicciones al futuro y las anomalías predichas. También se pueden
                          observar
                          eventos como cuando la célula se encuentra parada o los momentos en que la máquina
                          hace la
                          inyección.
                        </b-card-text>
                      </b-card-body>
                    </b-col>
                  </b-row>
                </b-card>
              </b-row>
              <b-row>
                <b-card no-body class="overflow-hidden">
                  <b-row no-gutters>
                    <b-col md="4">
                      <b-card-img :src="widget_Medidor" alt="Medidor" class="rounded-0">
                      </b-card-img>
                    </b-col>
                    <b-col md="8">
                      <b-card-body title="Medidor">
                        <b-card-text>
                          Este widget está pensado para la monitorización del valor en tiempo real de un sensor.
                        </b-card-text>
                      </b-card-body>
                    </b-col>
                  </b-row>
                </b-card>
              </b-row>
              <b-row>
                <b-card no-body class="overflow-hidden">
                  <b-row no-gutters>
                    <b-col md="4">
                      <b-card-img :src="widget_ApexGrafica" alt="Medidor" class="rounded-0">
                      </b-card-img>
                    </b-col>
                    <b-col md="8">
                      <b-card-body title="ApexGrafica">
                        <b-card-text>
                          Este widget está también pensado para la monitorización en tiempo real y en este caso
                          se
                          muestra una ventana de tiempo de las últimas mediciones y se agregan las predicciones
                          a
                          futuro de la última medición. También se puede visualizar los eventos como inyecciones
                          o
                          anomalías.
                        </b-card-text>
                      </b-card-body>
                    </b-col>
                  </b-row>
                </b-card>
              </b-row>
              <b-row>
                <b-card no-body class="overflow-hidden">
                  <b-row no-gutters>
                    <b-col md="4">
                      <b-card-img :src="widget_EchartsGrafica" alt="EchartsGrafica" class="rounded-0">
                      </b-card-img>
                    </b-col>
                    <b-col md="8">
                      <b-card-body title="EchartsGrafica">
                        <b-card-text>
                          Este widget está pensado para combinar los datos históricos con datos reales de manera que
                          primero carga una ventana de tiempo específica en el pasado desde base de datos y después se
                          empiezan a añadir valores en tiempo real mediante sockets. Este widget ha quedado en
                          desarrollo.
                        </b-card-text>
                      </b-card-body>
                    </b-col>
                  </b-row>
                </b-card>
              </b-row>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.forecasting variant="warning">Modelo de predicción al futuro</b-button>
          </b-card-header>
          <b-collapse id="forecasting" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-row>
                <b-col cols="6">
                  <b-img :src="forecasting_arch" fluid alt="Responsive image"></b-img>
                </b-col>
                <b-col cols="6">
                  <b-table stacked :items="forecastingmetadata"></b-table>
                  <b-img :src="forecasting_loss" fluid alt="Model Loss"></b-img>
                  <b-img :src="forecastingaccuracy" fluid alt="Responsive image"></b-img>
                </b-col>
              </b-row>
              <b-img :src="forecasting_test" fluid alt="Responsive image"></b-img>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.anomaly variant="warning">Modelo de anomalías</b-button>
          </b-card-header>
          <b-collapse id="anomaly" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-row>

                <b-card no-body class="overflow-hidden">
                  <b-row no-gutters>
                    <b-col md="12">
                      <b-card-img :src="anomalymodel_arch" alt="EchartsGrafica" class="rounded-0"
                        style="max-height: 400px !important">
                      </b-card-img>
                    </b-col>
                    <b-col md="12">
                      <b-card-img :src="anomalymodel" alt="EchartsGrafica" class="rounded-0">
                      </b-card-img>
                    </b-col>
                  </b-row>
                </b-card>
              </b-row>
            </b-card-body>
          </b-collapse>
        </b-card>
      </div>
    </b-modal>


    <b-modal id="modal-shutdown" no-fade header-bg-variant="secondary" header-text-variant="light">
      <template #modal-header>
        <h5>Shutdown</h5>
      </template>

      <template #default>
        <h5>Are you sure you want to power off the device ?</h5>
      </template>

      <template #modal-footer="{ ok, cancel }">
        <!-- Emulate built in modal footer ok and cancel button actions -->
        <b-button size="sm" variant="danger" @click="
  shutDown();
ok();
        ">OK</b-button>
        <b-button size="sm" variant="success" @click="cancel()">Cancel</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>

// Forecasting model
import forecasting_arch from "../img/forecasting_arch.png"
import forecasting_test from "../img/forecasting_test.png"
import forecastingmetadata from "../img/forecasting_metadata.json"
import forecastingaccuracy from "../img/forecasting_accuracy.png"
import forecasting_loss from "../img/forecasting_loss.png"
import partes_app from "../img/partes_app.png"
import opciones_widget from "../img/opciones_widget.png"
import barra_lateral from "../img/barra_lateral.png"
import widget_PlotlyGrafica from "../img/widget_PlotlyGrafica.png"
import widget_Medidor from "../img/widget_Medidor.png"
import widget_ApexGrafica from "../img/widget_ApexGrafica.png"
import widget_EchartsGrafica from "../img/widget_EchartsGrafica.png"

// Anomaly model
import anomalymodel from "../img/anomaly.png"
import anomalymodel_arch from "../img/anomaly_arch.png"

export default {
  data() {
    return {
      estado: "",
      piezas_ok: 0,
      forecasting_arch: forecasting_arch,
      forecasting_test: forecasting_test,
      forecastingmetadata: [forecastingmetadata],
      forecastingaccuracy: forecastingaccuracy,
      forecasting_loss: forecasting_loss,
      anomalymodel: anomalymodel,
      anomalymodel_arch: anomalymodel_arch,
      partes_app: partes_app,
      opciones_widget: opciones_widget,
      barra_lateral: barra_lateral,
      widget_PlotlyGrafica: widget_PlotlyGrafica,
      widget_Medidor: widget_Medidor,
      widget_ApexGrafica: widget_ApexGrafica,
      widget_EchartsGrafica: widget_EchartsGrafica,
      // msg: "No Message Received from Node-Red",
    };
  },
  methods: {
    shutDown() {
      uibuilder.send({
        cmd: "shutdown",
      });
      console.log("Message sent for Shutdown");
    },
  },
  mounted() {
    this.estado = "EN MARCHA"
    uibuilder.onChange("msg", (newMsg) => {
      if (this.estado == 0) {
        this.estado = "PARADA";
      }
      // this.estado = newMsg.celstate ? "EN MARCHA" : "PARADA";

      // this.piezas_ok = newMsg.cel_counter_ok;
      // console.info("Msg received from Node-RED server in Home:", newMsg);
    });
  },
};
</script>

<style scoped>
:host /deep/ .dropdown-item.router-link-exact-active,
:host /deep/ .dropdown-item:active {
  background-color: #a8a8a8 !important;
}

:host /deep/ .dropdown-item:active {
  background-color: #ffc107 !important;
}

.b-tooltip-danger {
  margin-right: 45px !important;
}

.b-tooltip-info {
  margin-right: 5px !important;
}

:host /deep/ .modal-header {
  padding: 0.2rem 1rem !important;
}

/* Buzz Out */
@-webkit-keyframes hvr-buzz-out {
  10% {
    -webkit-transform: translateX(3px) rotate(2deg);
    transform: translateX(3px) rotate(2deg);
  }

  20% {
    -webkit-transform: translateX(-3px) rotate(-2deg);
    transform: translateX(-3px) rotate(-2deg);
  }

  30% {
    -webkit-transform: translateX(3px) rotate(2deg);
    transform: translateX(3px) rotate(2deg);
  }

  40% {
    -webkit-transform: translateX(-3px) rotate(-2deg);
    transform: translateX(-3px) rotate(-2deg);
  }

  50% {
    -webkit-transform: translateX(2px) rotate(1deg);
    transform: translateX(2px) rotate(1deg);
  }

  60% {
    -webkit-transform: translateX(-2px) rotate(-1deg);
    transform: translateX(-2px) rotate(-1deg);
  }

  70% {
    -webkit-transform: translateX(2px) rotate(1deg);
    transform: translateX(2px) rotate(1deg);
  }

  80% {
    -webkit-transform: translateX(-2px) rotate(-1deg);
    transform: translateX(-2px) rotate(-1deg);
  }

  90% {
    -webkit-transform: translateX(1px) rotate(0);
    transform: translateX(1px) rotate(0);
  }

  100% {
    -webkit-transform: translateX(-1px) rotate(0);
    transform: translateX(-1px) rotate(0);
  }
}

@keyframes hvr-buzz-out {
  10% {
    -webkit-transform: translateX(3px) rotate(2deg);
    transform: translateX(3px) rotate(2deg);
  }

  20% {
    -webkit-transform: translateX(-3px) rotate(-2deg);
    transform: translateX(-3px) rotate(-2deg);
  }

  30% {
    -webkit-transform: translateX(3px) rotate(2deg);
    transform: translateX(3px) rotate(2deg);
  }

  40% {
    -webkit-transform: translateX(-3px) rotate(-2deg);
    transform: translateX(-3px) rotate(-2deg);
  }

  50% {
    -webkit-transform: translateX(2px) rotate(1deg);
    transform: translateX(2px) rotate(1deg);
  }

  60% {
    -webkit-transform: translateX(-2px) rotate(-1deg);
    transform: translateX(-2px) rotate(-1deg);
  }

  70% {
    -webkit-transform: translateX(2px) rotate(1deg);
    transform: translateX(2px) rotate(1deg);
  }

  80% {
    -webkit-transform: translateX(-2px) rotate(-1deg);
    transform: translateX(-2px) rotate(-1deg);
  }

  90% {
    -webkit-transform: translateX(1px) rotate(0);
    transform: translateX(1px) rotate(0);
  }

  100% {
    -webkit-transform: translateX(-1px) rotate(0);
    transform: translateX(-1px) rotate(0);
  }
}

.hvr-buzz-out {
  display: inline-block;
  font-size: 1.1rem;
  /* vertical-align: middle; */
  -webkit-transform: perspective(1px) translateZ(0);
  transform: perspective(1px) translateZ(0);
  box-shadow: 0 0 1px rgba(0, 0, 0, 0);
}

.hvr-buzz-out:hover,
.hvr-buzz-out:focus,
.hvr-buzz-out:active {
  -webkit-animation-name: hvr-buzz-out;
  animation-name: hvr-buzz-out;
  -webkit-animation-duration: 0.75s;
  animation-duration: 0.75s;
  -webkit-animation-timing-function: linear;
  animation-timing-function: linear;
  -webkit-animation-iteration-count: 1;
  animation-iteration-count: 1;
}

/* Establish a z-index  */
/deep/ .b-navbar {
  z-index: 100;

}
</style>
