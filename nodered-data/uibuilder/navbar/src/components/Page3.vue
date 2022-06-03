<template lang="html">
  <b-container fluid class="pr-5">
   <!-- <Grafica medname=0></Grafica>
   <Grafica medname=1></Grafica> -->
   <Grafica SignalID="Temp_Horno"></Grafica>
   <Medidor SignalID="Temp_Horno"></Medidor>
  </b-container>
</template>

<script>

import { defineComponent } from "@vue/composition-api";
import Grafica from "./Grafica.vue";
import Medidor from "./Medidor.vue";

export default {
  name: "page2",
  components: {
    Grafica,
    Medidor
},
  data() {
    return {
      // msg: "No Message Received from Node-Red",
    };
  },
  methods: {},

  mounted() {
    uibuilder.onChange("msg", (newMsg) => {
      // console.info("Msg received from Node-RED server in Page3:", newMsg);
    });
  },
};
</script>

<style scoped>
</style>
