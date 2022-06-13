#! /usr/bin/env python
# author: Achraf Hmimou (@aacraf)


from influxdb_client import InfluxDBClient
from sklearn.preprocessing import MinMaxScaler
import pandas as pd 
import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from numpy import array
# from numpy import hstack
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import RepeatVector
from tensorflow.keras.layers import TimeDistributed
from matplotlib import gridspec
import math

# import tensorflowjs as tfjs



def evaluate_forecast(y_test_inverse, yhat_inverse):
  mse_ = tf.keras.losses.MeanSquaredError()
  mae_ = tf.keras.losses.MeanAbsoluteError()
  mape_ = tf.keras.losses.MeanAbsolutePercentageError()
  mae = mae_(y_test_inverse,yhat_inverse)
  print('mae:', mae)
  mse = mse_(y_test_inverse,yhat_inverse)
  print('mse:', mse)
  mape = mape_(y_test_inverse,yhat_inverse)
  print('mape:', mape)


def inverse_transform(y_test, yhat):
 y_test_reshaped = y_test.reshape(-1, y_test.shape[-1])
 yhat_reshaped = yhat.reshape(-1, yhat.shape[-1])
 yhat_inverse = scaler.inverse_transform(yhat_reshaped)
 y_test_inverse = scaler.inverse_transform(y_test_reshaped)
 return yhat_inverse, y_test_inverse


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
  |> range(start: -12h)
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


## NullValues

med = med.dropna(thresh=med.shape[0]*0.7, axis=1) # 70 de los valores en la columna%
data = med.loc[:, (med != 0).any(axis=0)] # Valores a 0

# horizontally stack columns
dataset = data.values
scaler = MinMaxScaler(feature_range=(-1, 0))
scaled_data = scaler.fit_transform(dataset)

# Defines the rolling window
n_steps_in, n_steps_out = 1, 15


train = scaled_data[:-n_steps_out]
test = scaled_data[-n_steps_out:]

# Split into train and test sets
train = scaled_data[:-n_steps_out]
test = scaled_data[-n_steps_out:]



X_train, y_train = split_sequences(train, n_steps_in, n_steps_out)
X_test, y_test = split_sequences(test, n_steps_in, n_steps_out)



# the dataset knows the number of features, e.g. 2
n_features = X_train.shape[2]
# define model
model = Sequential()
model.add(LSTM(200, activation='relu', input_shape=(n_steps_in, n_features)))
model.add(RepeatVector(n_steps_out))
model.add(LSTM(200, activation='relu', return_sequences=True))
model.add(TimeDistributed(Dense(n_features)))
model.compile(optimizer='adam', loss='mse')

# fit model
model.fit(X_train, y_train, epochs=5)
model.summary()

model.save('/data/models/models/forecasting.h5')

# Save model
# filename="/data/models/models/forecasting.sav"
# pickle.dump(model, open(filename,'wb'))





# yhat = model.predict(X_test[0], verbose=1)
# yhat_inverse, y_test_inverse = inverse_transform(y_test, yhat)

# 


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

#     x_train_ticks = data.head(train_size).index
#     y_train = data.head(train_size)[med]
#     x_test_ticks = data.tail(len(data)-train_size).index

#     sns.lineplot(x=x_train_ticks, y=y_train, ax=ax, label='Train Set') #navajowhite
#     sns.lineplot(x=x_test_ticks, y=y_test_inverse[:,i], ax=ax, color='orange', label='Ground truth') #navajowhite
#     sns.lineplot(x=x_test_ticks, y=yhat_inverse[:,i], ax=ax, color='green', label='Prediction') #navajowhite
#     text = med + ' MAPE: ' + str(mape_(yhat_inverse[:,i], y_test_inverse[:,i]).numpy())
#     ax.title.set_text(text)
  
# fig.tight_layout()
# fig.savefig("/data/models/images/forecasting.png")

