<template>
  <div>
    <apexchart
      width="100%"
      height="50%"
      type="line"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

 <script>
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  name: "Grafica",
  props: {
    medname: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      options: {
        chart: {
          id: "vuechart-example",
        },
        colors: ["#FF0000", "#247BA0", "#FF0000"],
        title: {
          text: '',
          align: 'center',
          style: {
            fontSize:  '20px',
          },
        },
        annotations: {
          points: [],
          xaxis: []
        },
        forecastDataPoints: {
          count: 3
        },
        stroke : {
          curve: 'smooth',
        },
      },
      series: [
        {
          name: "",
          data: [],
        },
        {
          name: "",
          data: [],
        },
        {
          name: "",
          data: [],
        },
      ],

    };
  },
  methods: {
    initChart() {
      // this.series[0].data = [];
      // for (let i = 0; i < 10; i++) {
      //   this.series[0].data.push({x:new Date().getTime(), y: Math.random()});
      // }
    },
    updateChart(med, inyectada, anomalia) {
       let points = this.options.annotations.points;
       let xaxis = this.options.annotations.xaxis;
      //  console.log("inyectada", inyectada);

    let timestamp = med.timestamp;
    // let timestamp = new Date(med.timestamp);
    // timestamp = timestamp.getHours() + ":" + timestamp.getMinutes() + ":" + timestamp.getSeconds();
      if(inyectada)
        {
        points.push({
            x: timestamp,
            y: med.fields.value,
            marker: {
              size: 8,
              fillColor: '#fff',
              strokeColor: 'red',
              radius: 2,
              cssClass: 'apexcharts-custom-class'
            },
            label: {
              borderColor: '#FF4560',
              offsetY: 0,
              style: {
                color: '#fff',
                background: '#FF4560',
              },
        
              text: 'Inyectada',
            }
          }
        )
      }
      this.options = 
      {
        title: {
          text: med.tags.medicion,
          align: 'center',
          style: {
            fontSize:  '20px',
          },
        },
        annotations: {
          points: points,
          xaxis: xaxis
        },
      }

      let datapoint_value = { x: timestamp, y: med.fields.value };
      let datapoint_value_max = { x: timestamp, y: med.fields.value_max };
      let datapoint_value_min = { x: timestamp, y: med.fields.value_min };
      this.series[0].data.push(datapoint_value_max);
      this.series[1].data.push(datapoint_value);
      this.series[2].data.push(datapoint_value_min);
      // this.series = [...this.series];
      let newDataMax = this.series[0].data.slice(-40);
      let newData = this.series[1].data.slice(-40);
      let newDataMin = this.series[2].data.slice(-40);
      this.series = [
        {
          name: "Tolerancia Maxima",
          data: newDataMax,
        },
        {
          name: med.tags.medicion,
          data: newData,
        },
        {
          name: "Tolerancia Minima",
          data: newDataMin,
        },
      ];
    },

    addAnomaly(){
      let xaxis = this.options.annotations.xaxis;
      let points = this.options.annotations.points;

      // if(xaxis[xaxis.length-1].x == this.series[1].data[this.series[1].data.length-2].x)
      // {
      //   let lastAnotation = xaxis.pop();
      //   lastAnotation.x = this.series[1].data[this.series[1].data.length-1].x;
      //   xaxis.push(lastAnotation);
      // }else{
      xaxis.push({
          x: this.series[1].data[ this.series[1].data.length-2].x,
          x2: this.series[1].data[ this.series[1].data.length-1].x,
          fillColor: 'orange',
          // label: {
          //   // text: 'Anomalia'
          // }
        } 
        );
        this.options = 
        {
          annotations: {
            points: points,
            xaxis: xaxis
          },
            }
      // }
    }
  },
  mounted() {
    this.initChart();
    uibuilder.onChange("msg", (newMsg) => {
      if(newMsg.payload.anomalia)
      {
        this.addAnomaly();
      }else{
        this.updateChart(newMsg.payload[this.medname], newMsg.inyectada);
      }
    });
  },
});
</script>
 
