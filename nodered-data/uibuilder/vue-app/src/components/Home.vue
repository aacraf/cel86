<template>
  <b-container fluid class="pr-5">
    <h2 class="ml-4 mt-4">Dashboard</h2>
    <b-card>
      <b-card-header>
        <b-card-header-text>
          <b-icon icon="chart-bar"></b-icon>
          <span class="ml-3 mr-5">CEL86</span>
        </b-card-header-text>
      </b-card-header>
    </b-card> 
    <!-- <vue-json-pretty :deep="0" :showLength="true" :showDoubleQuotes="false" :showSelectController="true" :deepCollapseChildren="true" :data="msg" > </vue-json-pretty> -->
  </b-container>
</template>

<script>
import uibuilder from 'node-red-contrib-uibuilder/front-end/src/uibuilderfe.js'
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
