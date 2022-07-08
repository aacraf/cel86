
<template>
      <div>
        <VueSvgGauge
          :start-angle="parseInt(-110)"
          :end-angle="parseInt(110)"
          :value="value"
          :separator-step="0"
          :min="minvalue"
          :max="maxvalue"
          :gauge-color="[{ offset: 0, color: '#347AB0'}, { offset: 100, color: '#8CDFAD'}]"
        >
          <h4 class="customizer-title" style="margin: 70px 0px 5px 55px !important">{{this.SignalID}}</h4>
          <div class="inner-text inner-text--3"  style="margin: 5px 0px 5px 65px !important">
              <span>{{ value.toFixed(4) }}</span>
          </div>
        </VueSvgGauge>
      </div>
</template>
<script>
import { defineComponent } from "@vue/composition-api";
import moment from "moment";
import { VueSvgGauge } from 'vue-svg-gauge'

import 'moment/locale/es'  // without this line it didn't work
moment.locale('es')
export default defineComponent({
  props: {
    SignalID: {
      type: String,
      required: true,
    },
    stopLoading: {
      type: Function,
      required: false,
    },
  },
  components: {
    VueSvgGauge,
  },  
  data() {
    return {
      value: 0,
      maxvalue: 0,
      minvalue: 0,
      error: false,
    }
  },
  mounted() {
    uibuilder.onChange("msg", (newMsg) => {
      try{
        if (!this.maxvalue || !this.minvalue) {
          this.maxvalue = newMsg.payload.sensores.payload[this.SignalID+"_Max"];
          this.minvalue = newMsg.payload.sensores.payload[this.SignalID+"_Min"];
        }
        this.value = newMsg.payload.sensores.payload[this.SignalID];
      }
      catch(e){
      }
    });

    this.stopLoading();
    
  }
})

</script>

<style scoped>
    .customizer-title {
        font-size: 15px;
    }
    /* .inner-text {
      &--1, &--3 {
        display: flex;
        justify-content: center;
        margin-top: 85px;
        font-size: 20px;
        color: #de3a21;
        font-weight: bold;
        span { max-width: 100px };
      }
      &--3 {
        margin-top: 70px;
      }
      &--2 {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: #de3a21;
        font-weight: bold;
        span { max-width: 90px };
      } */
    /* } */

</style>