<template lang="html">
  <b-container fluid class="pr-5">
    <h2 class="ml-4 mt-4">Home</h2>
    <p>A ver cuando tarda</p>
    <p>Pues bastante</P>
    <p>a vale</p>
    <p>una ultima vez</p>
  </b-container>
</template>

<script>
export default {
  name: "home",
  data() {
    return {
      // msg: "No Message Received from Node-Red",
    };
  },
  methods: {},

  mounted() {
    uibuilder.onChange("msg", (newMsg) => {
      console.info("Msg received from Node-RED server in Home:", newMsg);
    });
  },
};
</script>

<style scoped>
</style>