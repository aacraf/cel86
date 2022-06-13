<template>
  <div>
    <navbar></navbar>
    <keep-alive :max="13">
    <router-view :key="$route.fullPath" /> 
    </keep-alive>
  </div>
</template>

<script>
// import Vue from "vue";
import navbar from "./NavBar.vue";
import uibuilder from 'node-red-contrib-uibuilder/front-end/src/uibuilderfe.js'

export default {
  name: "app",
  components: {
    navbar
  },

mounted() {
  
  // uibuilder.debug(true);
  // uibuilder.start('/vue-app', '/uibuilder/vendor/socket.io')
    
}

};
</script>


<style>
h2 {
font-weight: bold !important;
}
</style>
