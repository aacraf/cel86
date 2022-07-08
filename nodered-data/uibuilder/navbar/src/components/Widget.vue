<template>
    <smart-widget fullscreen refresh :title="this.type" @on-refresh="handleRefresh" :loading="loading"
        :key="componentKey">
        <template slot="editbox" v-if="alarm">
            <b-alert show :variant="alarm.type">{{ alarm.msg }}</b-alert>
        </template>
        <template slot="toolbar">
            <div style="margin: 0 12 5 10px;">
                <b-icon-x-square v-on:click="removeWidgetParent(gridindex)" size="1x"></b-icon-x-square>
            </div>
        </template>
        <div v-if="type == 'PlotlyGrafica'">
            <PlotlyGrafica :SignalID="SignalID" :timesteps="params.timesteps" :stopLoading="stopLoading">
            </PlotlyGrafica>
        </div>
        <div v-else-if="type == 'Medidor'">
            <Medidor :SignalID="SignalID" :stopLoading="stopLoading"></Medidor>
        </div>
        <div v-else-if="type == 'ApexGrafica'">
            <ApexGrafica :SignalID="SignalID" :stopLoading="stopLoading"></ApexGrafica>
        </div>
        <div v-else-if="type == 'EchartsGrafica'">
            <EchartsGrafica :SignalID="SignalID" :timesteps="params.timesteps" :stopLoading="stopLoading">
            </EchartsGrafica>
        </div>
    </smart-widget>
</template>

<script>

// import { PlotlyGrafica, Medidor, ApexGrafica, EchartsGrafica } from './Widgets';
import PlotlyGrafica from './Widgets/PlotlyGrafica.vue';
import Medidor from './Widgets/Medidor.vue';
import ApexGrafica from './Widgets/ApexGrafica.vue';
import EchartsGrafica from './Widgets/EchartsGrafica.vue';


export default {
    name: "widget",
    components: {
        PlotlyGrafica,
        Medidor,
        ApexGrafica,
        EchartsGrafica
    },
    props: {
        gridindex: {
            type: Number,
            required: false
        },
        removeWidget: {
            type: Function,
            required: false,
        },
        alarm: {
            type: Object,
            required: false,
            default: null
        },
        SignalID: {
            type: String,
            required: true,
        },
        type: {
            type: String,
            required: false,
            default: 'PlotlyGrafica',
        },
        params: {
            type: Object,
            required: false,
            default: {},
        },

    },
    data() {
        return {
            loading: true,
            componentKey: Math.random() * 1000,
        }
    },
    methods: {
        removeWidgetParent(index) {
            this.removeWidget(index);
        },
        handleRefresh(index) {
            this.loading = true;
            this.componentKey += 1;
            // setTimeout(() => {
            //     this.loading = false
            // }, 2000)
        },
        stopLoading() {
            this.loading = false;
        }
    }
    ,
}

</script>