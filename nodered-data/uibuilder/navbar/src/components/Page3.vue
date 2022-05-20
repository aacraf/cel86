<template lang="html">
  <b-container fluid class="pr-5">
   <!-- <Grafica medname=0></Grafica>
   <Grafica medname=1></Grafica> -->
   <Grafica medname=20></Grafica>
  </b-container>
</template>

<script>

import { defineComponent } from "@vue/composition-api";
import Grafica from "./Grafica.vue";
export default {
  name: "page2",
  components: {
    Grafica,
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
