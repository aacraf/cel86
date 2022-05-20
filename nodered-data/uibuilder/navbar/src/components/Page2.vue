
<template>
  <div>
    <apexchart type="treemap" height="800" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
<script>
import { defineComponent } from "@vue/composition-api";

export default defineComponent({

    data() {
      return {
          series: [
            {
              name: 'Lubrificador',
              data: [
                {
                  x: 'Flow_Cir_1',
                  y: 20
                },
                {
                  x: 'Flow_Cir_2',
                  y: 60
                },
                {
                  x: 'Flow_Cir_3',
                  y: 41
                },
                {
                  x: 'Flow_Cir_4',
                  y: 41
                }
              ]
            },
            {
              name: 'Parametros inyeccion',
              data: [
                {
                  x: 'Caudal_Piston',
                  y: 20
                },
                {
                  x: 'Pres_Final_Mult',
                  y: 20
                },
                {
                  x: 'Pres_Maxima_Mult',
                  y: 51
                },
                {
                  x: 'Tiempo_Mult',
                  y: 30
                },
                {
                  x: 'Tiempo_Subida_RT',
                  y: 20
                },
                {
                  x: 'Vel_1a_Fase_Maxima',
                  y: 30
                },
                                {
                  x: 'Vel_1a_Fase_Media',
                  y: 30
                },
                {
                  x: 'Vel_2a_Fase_Maxima',
                  y: 20
                },
                {
                  x: 'Vel_2a_Fase_Media',
                  y: 30
                }
              ]
            },
            {
              name: 'Instalaciones',
              data: [
                {
                  x: 'Pres_Entrada_Agua_Maquina',
                  y: 30
                },
                {
                  x: 'Pres_Entrada_Aire',
                  y: 60
                },
                {
                  x: 'Pres_Retorno_Agua_Maquina',
                  y: 41
                },
                  {
                  x: 'Pres_Retorno_Agua_Molde',
                  y: 41
                }
              ]
            },
                        {
              name: 'Temp Horno/Cuba/Pieza',
              data: [
                {
                  x: 'Temp_Cuba',
                  y: 30
                },
                {
                  x: 'Temp_Horno',
                  y: 30
                }
              ]
            },
          ],
          chartOptions: {
            legend: {
              show: true
            },
            chart: {
              height: 350,
              type: 'treemap',
              events: {
                  click: function(event, chartContext, config) {
                    // console.log(config.config.series[config.seriesIndex])
                    console.log(config.config.series[config.seriesIndex].name)
                    console.log(config.config.series[config.seriesIndex].data[config.dataPointIndex].x)
                  }        
              }
            },
            title: {
              text: 'Parámetros criticos CEL86',
              align: 'center'
            }
          },
      }
    },
    
  })

</script>