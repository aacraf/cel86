<template>
  <div>
    <b-navbar type="dark" variant="dark">
      <b-navbar-nav>
        <b-nav-text>
          <b-button variant="dark" v-b-toggle.sidebar-1>
            <b-icon-bezier2 animation="fade" style="animation-duration: 1.75s" scale="1.0" class="text-warning">
            </b-icon-bezier2>
          </b-button>
          <span class="ml-3 mr-5 hvr-buzz-out ">CEL86</span>
        </b-nav-text>
        <b-nav-item to="/" exact :active="$route.name == 'home'">Dashboard</b-nav-item>
        <b-nav-item to="/page1" exact :active="$route.name == 'page1'">Multivariable</b-nav-item>
        <b-nav-item to="/page2" exact :active="$route.name == 'page2'">Modelos</b-nav-item>
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
            <b-icon-info animation="fade" style="animation-duration: 1.75s" scale="1.5" class="text-warning">
            </b-icon-info>
          </b-button>
        </b-nav-item>
        <b-nav-item>
          <!-- ESTADO: {{this.estado}} -->
          <b-button variant="dark">v0.0</b-button>


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
      Información de los modelos
      <div class="accordion" role="tablist">
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.forecasting variant="warning">Modelo Forecasting</b-button>
          </b-card-header>
          <b-collapse id="forecasting" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-img :src="forecastingmodel" fluid alt="Responsive image"></b-img>
              <b-card-text>Explicar modelo.../b-card-text>
            </b-card-body>
          </b-collapse>
        </b-card>
        <b-card no-body class="mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-button block v-b-toggle.anomaly variant="warning">Modelo de Anomalias</b-button>
          </b-card-header>
          <b-collapse id="anomaly" accordion="my-accordion" role="tabpanel">
            <b-card-body>
              <b-img :src="anomalymodel" fluid alt="Responsive image"></b-img>
              <b-card-text>Explicar modelo...</b-card-text>
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
import forecastingmodel from "../img/forecasting.png"
import anomalymodel from "../img/anomaly.png"
export default {
  data() {
    return {
      estado: "",
      piezas_ok: 0,
      forecastingmodel: forecastingmodel,
      anomalymodel: anomalymodel,
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
