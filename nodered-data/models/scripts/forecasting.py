#! /usr/bin/env python
# author: Achraf Hmimou (@aacraf)
# basado en https://machinelearningmastery.com/how-to-develop-lstm-models-for-time-series-forecasting/

from influxdb_client import InfluxDBClient
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
import numpy as np
import time
from datetime import datetime
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec
import math
import json
import sys
import argparse

import tensorflow as tf
from numpy import array
# from numpy import hstack
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional
from tensorflow.keras.layers import Dense, Reshape, Dropout
from tensorflow.keras.layers import RepeatVector
from tensorflow.keras.layers import TimeDistributed

# Objeto donde se iran añadiendo datos del proceso
metadata = {}


### Parametros del script
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--window", dest = "window", default = "12h", help="Time window of data")
parser.add_argument("-e", "--epochs", dest = "epochs", default = 10, help="Epochs")
args = parser.parse_args()



#  Obtener diferentes metricas de evaluacion
def evaluate_forecast(y_test_inverse, yhat_inverse):
  mse_ = tf.keras.losses.MeanSquaredError()
  mae_ = tf.keras.losses.MeanAbsoluteError()
  mape_ = tf.keras.losses.MeanAbsolutePercentageError()
  rmse_ = tf.keras.metrics.RootMeanSquaredError()

  mae = mae_(y_test_inverse,yhat_inverse)
  print('mae:', mae)
  # metadata["mae test"] = str(mae.numpy())
  mse = mse_(y_test_inverse,yhat_inverse)
  # metadata["mse test"] = str(mse.numpy())
  print('mse:', mse)
  mape = mape_(y_test_inverse,yhat_inverse)
  # metadata["mape test"] = str(mape.numpy())
  print('mape:', mape)
  rmse = rmse_(y_test_inverse,yhat_inverse)
  # metadata["rmse test"] = str(rmse.numpy())
  print('rmse:', rmse)



# Realizar walk validation sobre una serie de datos
# Por cada punto de la serie, se realiza una prediccion y se evalua.
def walk_validation(dataset):
    
  predictions = []
  scores = []
  rmse_ = tf.keras.metrics.RootMeanSquaredError()

  for i, timestep in enumerate(dataset):
    timestep_reshape = timestep.reshape(1,n_steps_in,n_features)
    predicted = model.predict(timestep_reshape, verbose=0)
    if i+n_steps_out < len(dataset):
      test = dataset[i:i+n_steps_out]
      test = test.reshape(1,n_steps_out,n_features)
      predicted, test = inverse_transform(test, predicted)
      rmse = rmse_(test,predicted)
      scores.append(rmse.numpy())
    else:
      test = dataset[-n_steps_out:]
      predicted, test = inverse_transform(test, predicted)
    predictions.append(predicted[n_steps_out-1])
  
  return np.array(predictions), np.array(scores).mean()




# Fumciom que transforma de nuevo los datos de salida de la red neuronal a los datos 
def inverse_transform(y_test, yhat):
 y_test_reshaped = y_test.reshape(-1, y_test.shape[-1])
 yhat_reshaped = yhat.reshape(-1, yhat.shape[-1])
 yhat_inverse = scaler.inverse_transform(yhat_reshaped)
 y_test_inverse = scaler.inverse_transform(y_test_reshaped)
 return yhat_inverse, y_test_inverse

# Funcion que crea las sequencias de datos para la red neuronal
def split_sequences(sequences, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out
		# check if we are beyond the dataset
		if out_end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix:out_end_ix, :]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)




# Obtener datos de InfluxDB
my_token = "cie-token"
my_org = "cie"
bucket = "cel86"


metadata["ventana de tiempo"] = args.window
query = """
from(bucket: "cel86")
  |> range(start: -{0})
  |> filter(fn: (r) => r["_measurement"] == "sensores")
  |> filter(fn: (r) => r["molde"] == "MT201")
  |> filter(fn: (r) => r._field == "value")
  |> pivot(rowKey:["_time"], columnKey: ["medicion"], valueColumn: "_value")
  |> drop(columns: ["_start", "_stop", "_field", "_measurement", "molde"])
"""
query = query.format(args.window)


client = InfluxDBClient(url="http://influx-spc:8086/", token=my_token, org=my_org, debug=False)
med = client.query_api().query_data_frame(org=my_org, query=query)


# Preprocesado
if set(['result','table']).issubset(med.columns):
  med = med.drop(["result", "table"], axis=1)

med.set_index("_time", inplace = True)

## Valores nulos
med = med.dropna(thresh=med.shape[0]*0.7, axis=1) # 70 de los valores en la columna%
data = med.loc[:, (med != 0).any(axis=0)] # Valores a 0
data.interpolate(method ='linear', inplace=True)
metadata["numero de mediciones"] = data.shape[0]

## Escalar datos
scaler = MinMaxScaler(feature_range=(-1, 0))
dataset = scaler.fit_transform(data.values)

## Ventana de prediccion
n_steps_in, n_steps_out = 1, 20
metadata["pasos a predecir"] = n_steps_out

## Sets de entreno y test
test_size = round(len(data)*0.15)
train = dataset[:-test_size]
test = dataset[-test_size:]
metadata["conjunto de entrenamiento"] = len(data)-test_size 
metadata["conjunto de test"] = test_size
# obtener sequencias
X_train, y_train = split_sequences(train, n_steps_in, n_steps_out)
X_test, y_test = split_sequences(test, n_steps_in, n_steps_out)

## numero de variables de entrada
n_features = X_train.shape[2]
metadata["variables entrada"] = n_features
metadata["epochs"] = args.epochs

# Arquitectura del modelo
model = Sequential()
model.add(Bidirectional(LSTM(256, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features))))
model.add(Dropout(0.2))
model.add(LSTM(128, activation='relu'))
model.add(Dense(n_steps_out*n_features))
model.add(Reshape((n_steps_out,n_features)))
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

# Entrenamiento
init_train = datetime.now()
metadata["inicio entrenamiento"] = init_train.strftime("%d/%m/%Y %H:%M:%S")
history = model.fit(X_train, y_train, validation_split = 0.15, epochs=int(args.epochs))
end_train = datetime.now()
metadata["final entrenamiento"] = end_train.strftime("%d/%m/%Y %H:%M:%S")
metadata["tiempo entrenamiento"] = str((end_train - init_train))
model.summary()

# Guardar modelo
model.save('/data/models/models/forecasting.h5')

# Guardar resultados en el test de validación
plt.figure(figsize=(10,10))
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.savefig("/data/models/images/forecasting_accuracy.png")
plt.savefig("/data/uibuilder/navbar/src/img/forecasting_accuracy.png")

plt.figure(figsize=(10,10))
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.savefig("/data/models/images/forecasting_loss.png")
plt.savefig("/data/uibuilder/navbar/src/img/forecasting_loss.png")


# Evaluación mediante walk validation (proceso lento)
print("evaluando...")
predictions, rmse = walk_validation(test)

metadata["RMSE test"] = str(rmse)

test_inverse = scaler.inverse_transform(test)

# Graficar resultados de walk validation
from matplotlib import gridspec
import math
import tensorflow as tf

rmse_ = tf.keras.metrics.RootMeanSquaredError()

def do_plot(ax):
    ax.plot([1,2,3], [4,5,6], 'k.')

N = len(data.columns)
cols = 3
rows = int(math.ceil(N / cols))

gs = gridspec.GridSpec(rows, cols)
fig = plt.figure(figsize=(20, 15))
test_df = data[-test_size:]

for i, med in enumerate(test_df.columns):
    ax = fig.add_subplot(gs[i])

    # x_train_ticks = data.head(len(train)).index
    # y_train = data.head(len(train))[med]

    # ultimos 10 minutos del set de entrenamiento
    x_train_ticks = test_df.index
    x_model_ticks = test_df.index + pd.to_timedelta(20, unit='s')
    # y_train = data[-(n_steps_out+(10*60)):-n_steps_out][med]
    # x_test_ticks = data.tail(n_steps_out).index

    # sns.lineplot(x=x_train_ticks, y=y_train, ax=ax, label='Train Set') #navajowhite
    sns.lineplot(x=x_train_ticks, y=test_inverse[:,i], ax=ax, color='orange', label='Ground truth') #navajowhite
    sns.lineplot(x=x_model_ticks, y=predictions[:,i], ax=ax, color='green', label='Prediction') #navajowhite
    text = med + ' RMSE: ' + str(rmse_(predictions[:,i], test_inverse[:,i]).numpy())
    ax.title.set_text(text)
  
fig.tight_layout()


fig.savefig("/data/models/images/forecasting_test.png")
fig.savefig("/data/uibuilder/navbar/src/img/forecasting_test.png")


# plt.figure(figsize=(10,10))
# tf.keras.utils.plot_model(
#     model,
#     to_file='/data/uibuilder/navbar/src/img/forecasting_arch.png',
#     show_shapes=False,
#     show_dtype=False,
#     show_layer_names=True,
#     rankdir='TB',
#     expand_nested=False,
#     dpi=96
# )

# plt.savefig("/data/models/images/forecasting_arch.png")
# plt.savefig("/data/uibuilder/navbar/src/img/forecasting_arch.png")


# Test data prediction

# x_input = train[-1]
# x_input = x_input.reshape(1,n_steps_in,n_features)
# yhat = model.predict(x_input, verbose=1)      # predict values
# y_test = test.reshape(1,n_steps_out,n_features)
# yhat_inverse, y_test_inverse = inverse_transform(y_test, yhat)

# get test forecast metrics
# evaluate_forecast(y_test_inverse, yhat_inverse)


# # plot test forecast
# from matplotlib import gridspec
# import math
# import tensorflow as tf
# mape_ = tf.keras.losses.MeanAbsolutePercentageError()

# def do_plot(ax):
#     ax.plot([1,2,3], [4,5,6], 'k.')

# N = len(data.columns)
# cols = 3
# rows = int(math.ceil(N / cols))

# gs = gridspec.GridSpec(rows, cols)
# fig = plt.figure(figsize=(20, 15))
# for i, med in enumerate(data.columns):
#     ax = fig.add_subplot(gs[i])

#     # x_train_ticks = data.head(len(train)).index
#     # y_train = data.head(len(train))[med]

#     # ultimos 10 minutos del set de entrenamiento
#     x_train_ticks = data[-(n_steps_out+(10*60)):-n_steps_out].index
#     y_train = data[-(n_steps_out+(10*60)):-n_steps_out][med]
#     x_test_ticks = data.tail(n_steps_out).index

#     sns.lineplot(x=x_train_ticks, y=y_train, ax=ax, label='Train Set') #navajowhite
#     sns.lineplot(x=x_test_ticks, y=y_test_inverse[:,i], ax=ax, color='orange', label='Ground truth') #navajowhite
#     sns.lineplot(x=x_test_ticks, y=yhat_inverse[:,i], ax=ax, color='green', label='Prediction') #navajowhite
#     text = med + ' MAPE: ' + str(mape_(yhat_inverse[:,i], y_test_inverse[:,i]).numpy())
#     ax.title.set_text(text)



# Guardar datos de interes
print(metadata)
with open('/data/uibuilder/navbar/src/img/forecasting_metadata.json', 'w') as fp:
    json.dump(metadata, fp)
