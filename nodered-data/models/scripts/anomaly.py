#! /usr/bin/env python
# author: Achraf Hmimou (@aacraf)


from influxdb_client import InfluxDBClient
import pandas as pd 
import numpy as np
import time
import pickle
from adtk.data import validate_series
from adtk.detector import MinClusterDetector
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from adtk.visualization import plot


# InfluxDB Credentials
my_token = "cie-token"
my_org = "cie"
bucket = "cel86"

# Data - Retrival
# query= '''
# from(bucket: "cel86")
# |> range(start: -24h)
# |> filter(fn: (r) => r["_measurement"] == "Lubrificador")
# |> filter(fn: (r) => r["molde"] == "MT201")
# |> pivot(rowKey:["_time"], columnKey: ["medicion"], valueColumn: "_value")
# |> drop(columns: ["_start", "_stop", "_field", "_measurement", "molde"])'''


query = '''
from(bucket: "cel86")
  |> range(start: -6h)
  |> filter(fn: (r) => r["_measurement"] == "sensores")
  |> filter(fn: (r) => r["molde"] == "MT201")
  |> filter(fn: (r) => r._field == "value")
  |> pivot(rowKey:["_time"], columnKey: ["medicion"], valueColumn: "_value")
  |> drop(columns: ["_start", "_stop", "_field", "_measurement", "molde"])
'''


client = InfluxDBClient(url="http://influx-spc:8086/", token=my_token, org=my_org, debug=False)
med = client.query_api().query_data_frame(org=my_org, query=query)

if set(['result','table']).issubset(med.columns):
  med = med.drop(["result", "table"], axis=1)


med.set_index("_time", inplace = True)

# Data - Preprocessing

## NullValues

med = med.dropna(thresh=med.shape[0]*0.7, axis=1) # 70 de los valores en la columna%
med = med.loc[:, (med != 0).any(axis=0)] # Valores a 0



# print(med.head())

## Outliers
# Q1 = med.quantile(0.25)
# Q3 = med.quantile(0.75)
# IQR = Q3 - Q1
# med = med[~((med < (Q1 - 1.5 * IQR)) |(med > (Q3 + 1.5 * IQR))).any(axis=1)]



# Quality Simulation
# med["Calidad"] = np.random.choice((0,1,2), size = len(med), p=(0.2,0.5,0.3))


# Modeling

# X = med.drop(["Calidad"], axis=1)
# y = med['Calidad']

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


# classifier = RandomForestClassifier(max_depth=5, random_state=0)
# classifier.fit(X_train, y_train)

# # Predicting the Test set results
# y_pred = classifier.predict(X_test)

# cm = confusion_matrix(y_test, y_pred)
# print(cm)




anom = validate_series(med, check_freq=True)
min_cluster_detector = MinClusterDetector(KMeans(n_clusters=2))
anomalies = min_cluster_detector.fit_predict(anom)
plt.figure(figsize=(10,10))
plot(anom, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_color='red', anomaly_alpha=0.3, curve_group='all')
plt.savefig("/data/models/images/anomaly.png")


# print(classification_report(y_test, y_pred, target_names=["Mala", "Buena", "Excelente"]))
# print("Accuracy:", accuracy_score(y_test, y_pred))

# Save model
filename="/data/models/models/anomaly.sav"
pickle.dump(min_cluster_detector, open(filename,'wb'))

print("Todo OK.")
