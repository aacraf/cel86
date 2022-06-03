<template lang="html">
  <b-container fluid class="pr-5">
    <h2 class="ml-4 mt-4">Dashboard</h2>
    <b-img src="../assets/forecasting.png" fluid alt="Responsive image"></b-img>
    <!-- <vue-json-pretty :deep="0" :showLength="true" :showDoubleQuotes="false" :showSelectController="true" :deepCollapseChildren="true" :data="msg" > </vue-json-pretty> -->
  </b-container>
</template>

<script>
export default {
  name: "page1",
  data() {
    return {
       msg: "No Message Received from Node-Red",
    }
  },
  methods: {},

  mounted() {
    uibuilder.onChange("msg", (newMsg) => {
      // console.info("Msg received from Node-RED server in Page1:", newMsg);
      this.msg = newMsg
    });
  },
};
</script>

<style scoped>
</style>
