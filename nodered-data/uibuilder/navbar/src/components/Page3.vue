<template>
  <div>
    <apexchart
      width="50%"
      type="line"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

 <script>
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  data() {
    return {
      options: {
        chart: {
          id: "vuechart-example",
        }
      },
      series: [
        {
          name: "Flow_CIR_1",
          data: [],
        },
      ],
      xaxis: {
        type: 'datetime',
        max: 10,
      }
    };
  },
  methods: {

    initChart(){
      // this.series[0].data = [];
      // for (let i = 0; i < 10; i++) {
      //   this.series[0].data.push({x:new Date().getTime(), y: Math.random()});
      // }
    },
    updateChart(med) {
      console.log("updateChart med:", this.series[0].data);
      let datapoint = {x:med.timestamp, y: med.fields.value};
      this.series[0].data.push(datapoint);
      // this.series = [...this.series];
      let newData = this.series[0].data.slice(-100);
      this.series = [{
        name: "Flow_CIR_1",
        data: newData,
      }];
    },
  },
  mounted() {
    this.initChart();
    uibuilder.onChange("msg", (newMsg) => {
      this.updateChart(newMsg.payload[0]);
    });
  },
});
</script>
 
