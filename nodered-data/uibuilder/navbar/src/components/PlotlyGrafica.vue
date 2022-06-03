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
            default: '5h',
        },
    },
    data() {
        return {
            data: [{
                x: [],
                y: [],
                name: 'medicion',
                line: {
                    color: '#247BA0',
                    width: 2,
                },  
                // type: "scatter"
            }],
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
                shapes: []
            }
        }
    },
    methods: {
        updateChart(med) {
            console.log("med", med);
            let newData = this.data[0]
            if (med.timestamp != undefined) {
                newData.x.push(med.timestamp);
                newData.y.push(med.fields.value)
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
                console.log(response)
                response.forEach(row => {
                    this.data[0].x.push(row._time)
                    this.data[0].y.push(row.value);
                   
                    if(row.inyectada)
                    {
                        this.layout.annotations.push({
                            x: row._time,
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
                            x0: row._time,
                            // y0: 0,
                            x1: row._time,
                            // y1: row.value,
                            opacity: 0.1,
                            line: {
                                color: 'orange',
                                width: 0.5
                            }
                        })
                    }
                    if(!row.cel_state)
                    {
                        this.data[0].line.color = 'black';
                         this.data[0].text = "Maquina parada"
                    }

                })
            }
            //     this.live = true;
            // }
            // if (this.live) {
                // this.updateChart(newMsg.payload[newMsg.signal_index[this.SignalID]])
            // }
        })
    }
})
</script>