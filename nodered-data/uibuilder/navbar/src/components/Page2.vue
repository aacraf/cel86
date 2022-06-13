<template>
  <b-container fluid class="pr-5">
    <smart-widget-grid :layout="layout">
      <smart-widget slot="0" simple>
        <div class="layout-center">
          <h3>Simple Widget</h3>
        </div>
      </smart-widget>
      <smart-widget slot="1" title="Default Widget">
        <div class="layout-center">
          <h3>Widget with Header</h3>
        </div>
      </smart-widget>
      <smart-widget slot="2" title="Full Screen" fullscreen>
        <div class="layout-center">
          <h3>Make any widget full screen</h3>
        </div>
      </smart-widget>
      <div slot="3">
        <smart-widget  title="Prueba">
          <div class="layout-center">
            <h3>aver</h3>
          </div>
        </smart-widget>
      </div>
    </smart-widget-grid>

  </b-container>
</template>

<script>

// import Grafica from "./Grafica.vue";

export default{
 components: {
  //  Grafica
 },
 data () {
    return {
      layout: [
        { x: 0, y: 0, w: 4, h: 4, i: '0' },
        { x: 4, y: 0, w: 4, h: 4, i: '1' },
        { x: 8, y: 0, w: 4, h: 4, i: '2' },
        { x: 12, y: 2, w: 4, h: 4, i: '3' }
      ]
    }
  }
}
</script>
