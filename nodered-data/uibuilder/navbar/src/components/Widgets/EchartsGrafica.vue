<template>
  <div class="page-line-chart">
    <ve-line :x-axis="xAxis" :y-axis="yAxis" :title="title" :toolbox="toolbox" :tooltip="tooltip" :colors="chartColors" :data-zoom="chartDataZoom" :tooltip-visible="false" :series="series" :legend="legend" :resizeable="true" :mark-point="markPoint"></ve-line>
  </div>
</template>

<script>

import moment from 'moment';
moment.locale('es')

export default {
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
    this.chartDataZoom = [{ type: 'slider' }];
    this.markPoint = {
      data: [
      ]
    };
    return {
      legend: {
        data: ["Tolerancia Superior", "Medicion", "Modelo", "Tolerancia Inferior"],
        
        // data: [ "Medicion"],
        selected: {
          "Tolerancia Superior": false,
          "Medicion": true,
          "Modelo": false,
          "Tolerancia Inferior": false
          }
      },
      series: [
          {
          type: 'line',
          name: 'Tolerancia Superior',
          data: [],
          smooth: true,
          showSymbol: false,

        },
                        {
          type: 'line',
          name: 'Medicion',
          data: [],
          smooth: true,
          showSymbol: false,
        },
        {
          type: 'line',
          name: 'Modelo',
          data: [],
          smooth: true,
          showSymbol: false,
        },
        {
          type: 'line',
          name: 'Tolerancia Inferior',
          data: [],
          smooth: true,
          showSymbol: false,
        },
      ],
      xAxis: {
        type: "time",
        // boundaryGap: false,
        splitLine: {
          show: false
        }
      },
      yAxis: {
        type: "value",
        // boundaryGap: [0, "100%"],
        splitLine: {
          show: false
        },
        // boundaryGap: ['20%', '20%']

      },
      // visualMap: [{ type: "continuous" }],
      title: {
        textAlign: "left",
        text: this.SignalID,
        textStyle: {
          fontSize: 18,
          fontWeight: "bold"
        }
      },
      toolbox: {
        show: true,
        feature: {
          dataZoom: { yAxisIndex: "none" },
          restore: {},
          saveAsImage: {}
        }
      },
      tooltip: {
        trigger: "axis",
        axisPointer: {
          animation: false
        }
      },
      chartColors: [
        "#FF0000","#247BA0", "orange", "#FF0000"
      ],
      chartData: {
        showSymbol: false,
        columns: ["Timestamp", "Medicion"],
        rows: []
      }
    };
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
    uibuilder.send({ 'topic': 'queryInflux', 'payload': this.SignalID, 'query': fluxQuery })

    uibuilder.onChange("msg", (newMsg) => {
      // this.chartData.rows.push({
      //   'Timestamp': moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
      //   'Medicion': newMsg.payload.sensores.payload.Temp_Horno
      // })
      if (newMsg.topic == "queryInflux") {
          const response = JSON.parse(newMsg.payload);
           response.forEach(row => {
              this.series[0].data.push({
              name: moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
              value: [
                moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
                row.value_max
              ]})
              this.series[1].data.push({
              name: moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
              value: [
                moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
                row.value
              ]})
              this.series[2].data.push({
              name: moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
              value: [
                moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
                row.forecast_15
              ]})
              this.series[3].data.push({
              name: moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
              value: [
                moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
                row.value_min
              ]})

              if(row.inyectada)
              {
                this.markPoint.data.push({
                  name: 'Medicion',
                  yAxis: row.value,
                  xAxis: moment(row._time).format("YYYY-MM-DD HH:mm:ss"),
                  value: "Inyectada",
                })
              }
           })
           this.stopLoading();
           this.live = true;
      }
      if(this.live)
      {
        try{
          this.series[0].data.push({
              name: moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
              value: [
                moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
                newMsg.payload.sensores.payload[this.SignalID+"_Max"]
              ]
          })
          this.series[1].data.push({
            name: moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
            value: [
              moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
              newMsg.payload.sensores.payload[this.SignalID]
            ]
          })
           this.series[2].data.push({
            name: moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
            value: [
              moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
              newMsg.payload.forecasting.payload[14][newMsg.payload.forecasting.signal_index[this.SignalID]]
            ]
          })
           this.series[3].data.push({
            name: moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
            value: [
              moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
              newMsg.payload.sensores.payload[this.SignalID+"_Min"]
            ]
          })
  
          if(newMsg.payload.sensores.payload.Inyectada)
          {
            this.markPoint.data.push({
              name: 'Medicion',
              yAxis: newMsg.payload.sensores.payload[this.SignalID],
              xAxis: moment.utc(newMsg.payload.sensores.payload.FechaHora).format("YYYY-MM-DD HH:mm:ss"),
              value: "Inyectada",
            })
          }
        }
        catch(e){
          console.log(e)
        }
      }
    });

     
  }
};
</script>