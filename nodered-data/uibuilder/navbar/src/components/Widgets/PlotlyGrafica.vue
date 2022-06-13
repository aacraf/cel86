<template>
    <plotly :data="data" :layout="layout" :display-mode-bar="true" :displaylogo="false"></plotly>
</template>

<script>

import moment from 'moment';
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
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
            default: '2h',
        },
        stopLoading: {
            type: Function,
            required: false,
        },
    },
    data() {
        return {
            data: [
                {
                    x: [],
                    y: [],
                    name : 'Tolerancia Superior',
                    line: {
                        color: '#ff0000',
                        width: 2,
                    },
                    visible: 'legendonly',
                },
                {
                x: [],
                y: [],
                name: 'Medicion',
                line: {
                    color: '#247BA0',
                    width: 2,
                }
                },
                {
                    x: [],
                    y: [],
                    name : 'Modelo',
                    line: {
                        color: 'orange',
                        width: 2,
                    },
                    visible: 'legendonly',
                },
                {
                    x: [],
                    y: [],
                    name : 'Tolerancia Inferior',
                    line: {
                        color: '#ff0000',
                        width: 2,
                    },
                    visible: 'legendonly',
                } 
                // type: "scatter"
            ],
            layout: {
                title: this.SignalID,
                showlegend: true,
                // xaxix: {
                //     title: "Tiempo",
                //     type: "date",
                //     tickformat: "%H:%M:%S",
                //     // tick0: "0",
                //     dtick: "1s",
                //     // tickangle: "45",
                //     tickfont: {
                //         size: 10
                //     }
                // },
                xaxis: {
                    // rangeselector: ,selectorOptions
                    // rangeslider: {}
                },
                annotations: [],
                shapes: [],
                is_loading: true,
            }
        }
    },
    methods: {
        updateChart(med) {
            console.log("med", med);
            let newData = this.data[0]
            if (med.timestamp != undefined) {
                newData.x.push(med.FechaHora);
                newData.y.push(med[this.SignalID]);
                this.data[0] = newData;
            }
        }
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
            if (newMsg.topic == "queryInflux") {
                const response = JSON.parse(newMsg.payload);
                console.log("response", response);
                var forecastvalues = [];
                var timestamp;
                response.forEach(row => {
                    timestamp = moment(row._time).format("YYYY-MM-DD HH:mm:ss");
                    this.data[0].x.push(timestamp)
                    this.data[0].y.push(row.value_max);
                    this.data[1].x.push(timestamp)
                    this.data[1].y.push(row.value);
                    forecastvalues.push(parseFloat(row.forecast_15));
                    if(forecastvalues.length == 15) {
                        this.data[2].x.push(timestamp)
                        this.data[2].y.push(forecastvalues.shift());
                    }
                    this.data[3].x.push(timestamp)
                    this.data[3].y.push(row.value_min);
                    if(row.inyectada)
                    {
                        this.layout.annotations.push({
                            x: timestamp,
                            y: row.value,
                            xref: "x",
                            yref: "y",
                            arrowhead: 4,
                            ax: 0,
                            arrowsize: 1,
                            arrowwidth: 0.9,
                            arrowcolor: "red",
                            arrowside: "end",
                        })
                    }
                    if(row.anomalia)
                    {
                        this.layout.shapes.push({
                            type: 'line',
                            x0: timestamp,
                            // y0: 0,
                            x1: timestamp,
                            // y1: row.value,
                            opacity: 0.1,
                            line: {
                                color: 'orange',
                                width: 0.5
                            }
                        })
                    }
   
                    // if(!row.cel_state)
                    // {
                    //     this.data[0].line.color = 'black';
                    //     this.data[0].text = "Maquina parada"
                    // }

                })
                while(forecastvalues.length > 0)
                {
                    timestamp = moment(timestamp).add(1, 'second').format("YYYY-MM-DD HH:mm:ss")
                    this.data[2].x.push(timestamp)
                    this.data[2].y.push(forecastvalues.shift());
                }

                this.stopLoading();
            }
            //     this.live = true;
            // }
            // if (this.live) {
                // this.updateChart(newMsg.payload.sensores.payload);
            // }
        })
    }
})
</script>