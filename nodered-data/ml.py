#! /usr/bin/env python
# author: Achraf Hmimou (@aacraf)


from influxdb_client import InfluxDBClient
import pandas as pd 
import numpy as np
import time
import pickle


# InfluxDB Credentials
my_token = "some-token"
my_org = "cie"
bucket = "some-bucket"

# Data - Retrival
query= '''
from(bucket: "some-bucket")
|> range(start: -24h)
|> filter(fn: (r) => r["_measurement"] == "Instalaciones")
|> filter(fn: (r) => r["molde"] == "MT201")
|> pivot(rowKey:["_time"], columnKey: ["medicion"], valueColumn: "_value")
|> drop(columns: ["_start", "_stop", "_field", "_measurement", "molde"])'''
client = InfluxDBClient(url="http://influx-spc:8086/", token=my_token, org=my_org, debug=False)
med = client.query_api().query_data_frame(org=my_org, query=query)
med = med.drop(["result", "table", "_time"], axis=1)
print(med.head())

# Data - Preprocessing

## NullValues
med = med.dropna()

## Outliers
Q1 = med.quantile(0.25)
Q3 = med.quantile(0.75)
IQR = Q3 - Q1
med = med[~((med < (Q1 - 1.5 * IQR)) |(med > (Q3 + 1.5 * IQR))).any(axis=1)]



# Quality Simulation
med["Calidad"] = np.random.choice((0,1,2,3), size = len(med), p=(0.1,0.5, 0.2, 0.2))

print(med.head())

# Modeling

X = med.drop(["Calidad"], axis=1)
y = med['Calidad']

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


classifier = RandomForestClassifier(max_depth=5, random_state=0)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
print(cm)
print('Accuracy',accuracy_score(y_test, y_pred))

# Save model
filename="model.sav"
pickle.dump(classifier, open(filename,'wb'))