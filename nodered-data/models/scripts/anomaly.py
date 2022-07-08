#! /usr/bin/env python
# author: Achraf Hmimou (@aacraf)


from influxdb_client import InfluxDBClient
import pandas as pd 
import numpy as np
import time
import pickle
from adtk.data import validate_series
from adtk.detector import MinClusterDetector
from adtk.detector import PcaAD
from adtk.visualization import plot
from sklearn.cluster import KMeans
from adtk.transformer import PcaProjection
from adtk.pipe import Pipenet
import matplotlib.pyplot as plt
import argparse



# Parametros del script
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--window", dest = "window", default = "72h", help="Time window of data")
args = parser.parse_args()


# Obtener datos de InfluxDB
my_token = "cie-token"
my_org = "cie"
bucket = "cel86"

query = '''
from(bucket: "cel86")
  |> range(start: -{0})
  |> filter(fn: (r) => r["_measurement"] == "sensores")
  |> filter(fn: (r) => r["molde"] == "MT201")
  |> filter(fn: (r) => r._field == "value")
  |> pivot(rowKey:["_time"], columnKey: ["medicion"], valueColumn: "_value")
  |> drop(columns: ["_start", "_stop", "_field", "_measurement", "molde"])
'''
query = query.format(args.window)

client = InfluxDBClient(url="http://influx-spc:8086/", token=my_token, org=my_org, debug=False)
med = client.query_api().query_data_frame(org=my_org, query=query)



# Preprocesado de datos
if set(['result','table']).issubset(med.columns):
  med = med.drop(["result", "table"], axis=1)

med.set_index("_time", inplace = True)

# valores nulos
med = med.dropna(thresh=med.shape[0]*0.7, axis=1) # 70 de los valores en la columna%
med = med.loc[:, (med != 0).any(axis=0)] # Valores a 0
# med.interpolate(method ='linear', inplace=True)

anom = validate_series(med, check_freq=True)


# Modeling
# Creando pipenet
steps = {
    "pca": {
        "model": PcaProjection(k=6),
        "input": "original"
    },
    
    "kmeans": {
        "model": MinClusterDetector(KMeans(n_clusters=2)),
        "input": "pca",
    },
    # "output": {
    #     "model": AndAggregator(),
    #     "input": ["kmeans"]
    # }
}
pipenet = Pipenet(steps)

plt.figure(figsize=(10,10))
pipenet.summary()
pipenet.plot_flowchart();
plt.savefig("/data/models/images/anomaly_arch.png")
plt.savefig("/data/uibuilder/navbar/src/img/anomaly_arch.png")

# Ejecutando pipenet
anomalies = pipenet.fit_detect(anom)

# Guardar resultados para la evaluación
plt.figure(figsize=(10,10))
plot(anom, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_color='red', anomaly_alpha=0.3, curve_group='all')
plt.savefig("/data/models/images/anomaly.png")
plt.savefig("/data/uibuilder/navbar/src/img/anomaly.png")

# Guardar modelo
filename="/data/models/models/anomaly.sav"
pickle.dump(pipenet, open(filename,'wb'))

print("Todo OK.")
