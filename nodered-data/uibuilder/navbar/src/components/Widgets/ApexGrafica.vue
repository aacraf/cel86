<template>
  <div>
    <apexchart
      width="100%"
      height="100%"
      type="line"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

 <script>
import { defineComponent } from "@vue/composition-api";
import moment from "moment";

import 'moment/locale/es'  // without this line it didn't work
moment.locale('es')


// import { InfluxDB, Point } from '@influxdata/influxdb-client'

// const queryApi = new InfluxDB({url:'http://influx-spc:8086/', token:'cie-token'}).getQueryApi('cie')



export default defineComponent({
  name: "Grafica",
  props: {
    SignalID: {
      type: String,
      required: true,
    },
    live: {
      type: Boolean,
      required: false,
      default: false,
    },
    timesteps: {
      type: String,
      required: false,
      default: '5m',
    },
    stopLoading: {
      type: Function,
      required: false,
    },
  },
  data() {
    return {
      options: {
        chart: {
          id: "vuechart-example",
          animations: {
            enabled: true,
            easing: 'linear',
            dynamicAnimation: {
              speed: 1000
            }
          }
        },
        colors: ["#247BA0"],
        fill: {
          type: "gradient",
        },
        dataLabels: {
          enabled: false
        },
        title: {
          text: this.SignalID,
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
          count: 20
        },
        stroke : {
          curve: 'smooth',
          dashArray: [0, 0, 5, 0],
        },
        xaxis: {
          // type: 'datetime',
          // range: 20,
          labels: {            
            type: 'datetime',
            show: true,
            formatter: function (val, timestamp) {
              let time = moment(timestamp)
              time = time.format('HH:mm:ss')
              return time;
            },
          }
        }
      },
      series: [
        {
          name: "Medicion",
          data: [],
        },
      ],

    };
  },
  methods: {
    updateChart(med, anomalia) {
       let points = this.options.annotations.points;
       let xaxis = this.options.annotations.xaxis;

      let timestamp =  moment(med.sensores.payload.FechaHora,'YYYY-MM-DD HH:mm:ss').valueOf();
      let inyectada = med.sensores.payload.Inyectada;
      if(inyectada)
      {
        points.push({
            x: timestamp,
            y: med.sensores.payload[this.SignalID],
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
          })
        this.options = {...this.options,
          annotations: {
            points: points,
            xaxis: xaxis
          },
        }
      }

      if(anomalia)
      {
        this.addAnomaly();
      }

      if(this.series[0].data.length)
      {
        for(let i = 0; i<20; i++)
        {
          this.series[0].data.pop()
        }

        if(this.series[0].data.length > 80)
        {
          this.series[0].data.shift()
        }
      }
      this.series[0].data.push({ x: timestamp, y: med.sensores.payload[this.SignalID].toFixed(3) });
      for(let i = 0; i<20; i++)
      {
        timestamp = moment(timestamp).add(1, 'second').valueOf()
        this.series[0].data.push({x:timestamp, y: med.forecasting.payload[i][med.forecasting.signal_index[this.SignalID]].toFixed(3)})
      }
      this.series = [...this.series];
    },

    addAnomaly(){
      let xaxis = this.options.annotations.xaxis;
      let points = this.options.annotations.points;
      xaxis.push({
          x: this.series[0].data[ this.series[0].data.length-(2+20)].x,
          x2: this.series[0].data[ this.series[0].data.length-(1+20)].x,
          fillColor: 'red',
      });
      this.options = 
      {...this.options,
        annotations: {
          points: points,
          xaxis: xaxis
        },
      }
    },
  },
  mounted() {
    const fluxQuery = `
      from(bucket: "cel86")
        |> range(start: -${this.timesteps})
        |> filter(fn: (r) => r["_measurement"] == "sensores")
        |> filter(fn: (r) => r["molde"] == "MT201")
        |> filter(fn: (r) => r["medicion"] == "${this.SignalID}")
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> drop(columns: ["_start", "_stop", "_measurement"])
    `
    // uibuilder.send( { 'topic': 'queryInflux', 'payload': this.SignalID, 'query': fluxQuery} )

    uibuilder.onChange("msg", (newMsg) => {

      // if(newMsg.topic == "queryInflux")
      // {
      //   const response = JSON.parse(newMsg.payload);
      //   // console.log("INIT DATA: ", JSON.parse(newMsg.payload));
      //   // let initData = [];
      //   response.forEach(row => {
      //     // this.series[0].data.push({ x: moment(row._time).valueOf(),  y: row.value_min});
      //     this.series[1].data.push({ x: moment(row._time).valueOf(),  y: row.value});
      //     // this.series[3].data.push({ x: moment(row._time).valueOf(),  y: row.value_max});
      //   })
      //   this.options = {...this.options, title: { text: this.SignalID }};
      //   this.series = [...this.series];
      // }
      // if(newMsg.payload.anomalia)
      // {
      //   this.addAnomaly();
      // }
      // if(newMsg.payload.forecasting){
      //   this.addForecasting(newMsg.payload.forecasting);
      // }
      // else{
      //   }
      // if (newMsg.payload[this.SignalID].timestamp == this.series[1].data[this.series[1].data.length-1].x)
      // {
      //   this.live = true;   
      // }
      // if(this.live)
      // {

        try{
          this.updateChart(newMsg.payload, newMsg.payload.anomalia.payload[0]);
        }
        catch(e){
          console.log("Error: ", e);
        }

      // }
    });

    this.stopLoading();
  }
  
});
</script>
 
