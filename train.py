import pandas as pd
import numpy as np
import tensorflow as tf
import requests
from datetime import datetime, timedelta
import time as sleep
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

api_url_data = 'https://api.covid19india.org/data.json'
r_data = requests.get(api_url_data)
data_time_series = r_data.json()

time = data_time_series.get('cases_time_series')

date_list = []
dailyconfirmed_list = []
dailydeceased_list = []
dailyrecovered_list = []
dailyactive_list = []

totalconfirmed_list = []
totaldeceased_list = []
totalrecovered_list = []
totalactive_list = []

t = 0
for t in range(len(time)):
    
    date = time[t].get('date')
    date_list.append(date)
    
    dailyconfirmed = int(time[t].get('dailyconfirmed'))
    dailyconfirmed_list.append(dailyconfirmed)
    
    dailydeceased = int(time[t].get('dailydeceased'))
    dailydeceased_list.append(dailydeceased)
    
    dailyrecovered = int(time[t].get('dailyrecovered'))
    dailyrecovered_list.append(dailyrecovered)
    
    totalconfirmed = int(time[t].get('totalconfirmed'))
    totalconfirmed_list.append(totalconfirmed)
    
    totalrecovered = int(time[t].get('totalrecovered'))
    totalrecovered_list.append(totalrecovered)
    
    totaldeceased = int(time[t].get('totaldeceased'))
    totaldeceased_list.append(totaldeceased)
    
daily_data = {'Daily Confirmations':dailyconfirmed_list[-14:], 'Daily Recoveries':dailyrecovered_list[-14:], 'Daily Deaths':dailydeceased_list[-14:], 'Total Confirmations':totalconfirmed_list[-14:], 'Total Recoveries':totalrecovered_list[-14:], 'Total Deaths':totaldeceased_list[-14:]}
df_daily_data = pd.DataFrame(daily_data, index = [date_list[-14:]])
print(df_daily_data)
    
totalconfirmed_list = np.array(totalconfirmed_list, dtype=int)
totalrecovered_list = np.array(totalrecovered_list, dtype=int)
totaldeceased_list = np.array(totaldeceased_list, dtype=int)

dailyconfirmed_list = np.array(dailyconfirmed_list, dtype=int)
dailyrecovered_list = np.array(dailyrecovered_list, dtype=int)
dailydeceased_list = np.array(dailydeceased_list, dtype=int)


day_range_train = -28

x_conf = totalconfirmed_list[day_range_train:]
x_rec = totalrecovered_list[day_range_train:]
x_det = totaldeceased_list[day_range_train:]

pd_pred_report = pd.read_csv(os.path.join(dir_path, 'CSV', 'PRED_REPORTS.csv'))

pd_pred_list_conf = pd_pred_report['pred_list_conf'].values
pd_pred_list_rec = pd_pred_report['pred_list_rec'].values
pd_pred_list_det = pd_pred_report['pred_list_det'].values

pd_conf_loss = pd_pred_report['conf_loss'].values
pd_rec_loss = pd_pred_report['rec_loss'].values
pd_det_loss = pd_pred_report['det_loss'].values

i,j,k,l,m,n = 0,0,0,0,0,0

pred_list_conf = []
pred_list_rec = []
pred_list_det = []

conf_loss = []
rec_loss = []
det_loss = []

for i in pd_pred_list_conf:
    pred_list_conf.append(i)
    
for j in pd_pred_list_rec:
    pred_list_rec.append(j)
    
for k in pd_pred_list_det:
    pred_list_det.append(k)
    
for l in pd_conf_loss:
    conf_loss.append(l)
    
for m in pd_rec_loss:
    rec_loss.append(m)
    
for n in pd_det_loss:
    det_loss.append(n)
    
window_size = 3

with tf.device('/CPU:0'):        
    dataset = tf.data.Dataset.from_tensor_slices(x_conf)
    dataset = dataset.window(window_size+1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.map(lambda window: (window[:-1], window[-1:]))
    dataset = dataset.shuffle(buffer_size=len(x_conf))
    dataset = dataset.batch(1).prefetch(1)
    
    for x,y in dataset:
        print(x.numpy(), y.numpy())


    pred_list_conf = []
    pred_list_rec = []
    pred_list_det = []

    conf_loss = []
    rec_loss = []
    det_loss = []

    iterations = 3
    epoch = 10000
    patience = 2000

    i = 0
    for i in range(iterations):
        dataset = tf.data.Dataset.from_tensor_slices(x_conf)
        dataset = dataset.window(window_size+1, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
        dataset = dataset.map(lambda window: (window[:-1], window[-1:]))
        dataset = dataset.shuffle(buffer_size=len(x_conf))
        dataset = dataset.batch(1).prefetch(1)

        callback = [tf.keras.callbacks.EarlyStopping(monitor = 'loss', min_delta = 0.0001, patience = patience, verbose=1, mode = 'min', restore_best_weights = True),
                    tf.keras.callbacks.ModelCheckpoint(os.path.join(dir_path, 'MODEL', 'best_model_conf.h5'), monitor = 'loss', verbose=1, save_best_only=True, save_weights_only=False, mode = 'min' , period=1)]

        model_conf = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_conf.h5'))
        
        for layers in model_conf.layers:
            layers.trainable = True

        model_conf.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        history = model_conf.fit(dataset, epochs=epoch, verbose=1, callbacks=callback)

        loss = min(history.history['loss'])
        conf_loss.append(loss)

        pred_daily = model_conf.predict(x_conf[-window_size:][np.newaxis])
        pred_daily = int(pred_daily[0][0])
        pred_list_conf.append(pred_daily)

    j = 0
    for j in range(iterations):
        dataset = tf.data.Dataset.from_tensor_slices(x_rec)
        dataset = dataset.window(window_size+1, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
        dataset = dataset.map(lambda window: (window[:-1], window[-1:]))
        dataset = dataset.shuffle(buffer_size=len(x_rec))
        dataset = dataset.batch(1).prefetch(1)

        callback = [tf.keras.callbacks.EarlyStopping(monitor = 'loss', min_delta = 0.0001, patience = patience, verbose=1, mode = 'min', restore_best_weights = True),
                    tf.keras.callbacks.ModelCheckpoint(os.path.join(dir_path, 'MODEL', 'best_model_rec.h5'), monitor = 'loss', verbose=1, save_best_only=True, save_weights_only=False, mode = 'min' , period=1)]

        model_rec = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_rec.h5'))
        
        for layers in model_rec.layers:
            layers.trainable = True
        
        
        model_rec.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        history = model_rec.fit(dataset, epochs=epoch, verbose=1, callbacks=callback)

        loss = min(history.history['loss'])
        rec_loss.append(loss)

        pred_daily = model_rec.predict(x_rec[-window_size:][np.newaxis])
        pred_daily = int(pred_daily[0][0])
        pred_list_rec.append(pred_daily)

    k = 0
    for k in range(iterations):
        dataset = tf.data.Dataset.from_tensor_slices(x_det)
        dataset = dataset.window(window_size+1, shift=1, drop_remainder=True)
        dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
        dataset = dataset.map(lambda window: (window[:-1], window[-1:]))
        dataset = dataset.shuffle(buffer_size=len(x_det))
        dataset = dataset.batch(1).prefetch(1)

        callback = [tf.keras.callbacks.EarlyStopping(monitor = 'loss', min_delta = 0.0001, patience = patience, verbose=1, mode = 'min', restore_best_weights = True),
                    tf.keras.callbacks.ModelCheckpoint(os.path.join(dir_path, 'MODEL', 'best_model_det.h5'), monitor = 'loss', verbose=1, save_best_only=True, save_weights_only=False, mode = 'min' , period=1)]

        model_det = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_det.h5'))
        
        for layers in model_det.layers:
            layers.trainable = True

        model_det.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=0.001))
        history = model_det.fit(dataset, epochs=epoch, verbose=1, callbacks=callback)

        loss = min(history.history['loss'])
        det_loss.append(loss)

        pred_daily = model_det.predict(x_det[-window_size:][np.newaxis])
        pred_daily = int(pred_daily[0][0])
        pred_list_det.append(pred_daily)
        
        
model_conf = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_conf.h5'))
model_rec = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_rec.h5'))
model_det = tf.keras.models.load_model(os.path.join(dir_path, 'MODEL', 'best_model_det.h5'))
    
pred_reports = {"pred_list_conf":pred_list_conf, "pred_list_rec":pred_list_rec, "pred_list_det":pred_list_det, "conf_loss":conf_loss, "rec_loss":rec_loss, "det_loss":det_loss}
df_pred_reports = pd.DataFrame(pred_reports)
df_pred_reports.to_csv(os.path.join(dir_path, 'CSV', 'PRED_REPORTS.csv'))

pred_conf_lmin = pred_list_conf[conf_loss.index(min(conf_loss))]
pred_rec_lmin = pred_list_rec[rec_loss.index(min(rec_loss))]
pred_det_lmin = pred_list_det[det_loss.index(min(det_loss))]
pred_act_lmin = pred_conf_lmin - (pred_rec_lmin + pred_det_lmin)

pred_conf_max = pred_conf_lmin + pred_conf_lmin//100
pred_rec_max = pred_rec_lmin + pred_rec_lmin//100
pred_det_max = pred_det_lmin + pred_det_lmin//100
pred_act_max = pred_act_lmin + pred_act_lmin//100

pred_conf_min = pred_conf_lmin - pred_conf_lmin//200
pred_rec_min = pred_rec_lmin - pred_rec_lmin//100
pred_det_min = pred_det_lmin - pred_det_lmin//200
pred_act_min = pred_act_lmin - pred_act_lmin//200

pred = pred_conf_lmin-x_conf[-1]
pred_high = pred_conf_max-x_conf[-1]
pred_low = pred_conf_min-x_conf[-1]

if pred_conf_min < pred_conf_max:
    pred_conf_low = pred_conf_min
    pred_conf_high = pred_conf_max
else:
    pred_conf_low = pred_conf_max
    pred_conf_high = pred_conf_min
    
if pred_act_min < pred_act_max:
    pred_act_low = pred_act_min
    pred_act_high = pred_act_max
else:
    pred_act_low = pred_act_max
    pred_act_high = pred_act_min
    
if pred_rec_min < pred_rec_max:
    pred_rec_low = pred_rec_min
    pred_rec_high = pred_rec_max
else:
    pred_rec_low = pred_rec_max
    pred_rec_high = pred_rec_min
    
if pred_det_min < pred_det_max:
    pred_det_low = pred_det_min
    pred_det_high = pred_det_max
else:
    pred_det_low = pred_det_max
    pred_det_high = pred_det_min
    
pred_conf = str(pred_conf_low) + ' to ' + str(pred_conf_high)
pred_act = str(pred_act_low) + ' to ' + str(pred_act_high)
pred_rec = str(pred_rec_low) + ' to ' + str(pred_rec_high)
pred_det = str(pred_det_low) + ' to ' + str(pred_det_high)

x_conf_high = np.append(x_conf,pred_conf_high)
x_rec_high = np.append(x_rec, pred_rec_high)
x_det_high = np.append(x_det, pred_det_high)
x_act_high = np.array(x_conf_high-(x_rec_high + x_det_high))

x_conf_low = np.append(x_conf, pred_conf_low)
x_rec_low = np.append(x_rec, pred_rec_low)
x_det_low = np.append(x_det, pred_det_low)
x_act_low = np.array(x_conf_low-(x_rec_low + x_det_low))

reports = pd.read_csv(os.path.join(dir_path, 'CSV', 'REPORTS.csv'))

x_conf_long_pred = reports['x_conf_long_pred'].values[0]
x_act_long_pred = reports['x_act_long_pred'].values[0]
x_rec_long_pred = reports['x_rec_long_pred'].values[0]
x_det_long_pred = reports['x_det_long_pred'].values[0]

x_conf_high_long = x_conf_high
x_act_high_long = x_act_high
x_rec_high_long = x_rec_high
x_det_high_long = x_det_high

x_conf_low_long = x_conf_low
x_act_low_long = x_act_low
x_rec_low_long = x_rec_low
x_det_low_long = x_det_low

i = 0
for i in range(14):
    pred_daily = int(model_conf.predict(x_conf_high_long[-window_size:][np.newaxis]))
    x_conf_high_long = np.append(x_conf_high_long, pred_daily)

    pred_daily = int(model_conf.predict(x_act_high_long[-window_size:][np.newaxis]))
    x_act_high_long = np.append(x_act_high_long, pred_daily)

    pred_daily = int(model_conf.predict(x_rec_high_long[-window_size:][np.newaxis]))
    x_rec_high_long = np.append(x_rec_high_long, pred_daily)

    pred_daily = int(model_conf.predict(x_det_high_long[-window_size:][np.newaxis]))
    x_det_high_long = np.append(x_det_high_long, pred_daily)

    pred_daily = int(model_conf.predict(x_conf_low_long[-window_size:][np.newaxis]))
    x_conf_low_long = np.append(x_conf_low_long, pred_daily)

    pred_daily = int(model_conf.predict(x_act_low_long[-window_size:][np.newaxis]))
    x_act_low_long = np.append(x_act_low_long, pred_daily)

    pred_daily = int(model_conf.predict(x_rec_low_long[-window_size:][np.newaxis]))
    x_rec_low_long = np.append(x_rec_low_long, pred_daily)

    pred_daily = int(model_conf.predict(x_det_low_long[-window_size:][np.newaxis]))
    x_det_low_long = np.append(x_det_low_long, pred_daily)

x_conf_long_high_pred = int(x_conf_high_long[-1])
x_act_long_high_pred = int(x_act_high_long[-1])
x_rec_long_high_pred = int(x_rec_high_long[-1])
x_det_long_high_pred = int(x_det_high_long[-1])

x_conf_long_low_pred = int(x_conf_low_long[-1])
x_act_long_low_pred = int(x_act_low_long[-1])
x_rec_long_low_pred = int(x_rec_low_long[-1])
x_det_long_low_pred = int(x_det_low_long[-1])


x_conf_high_14 = x_conf_high_long[-14:]
x_act_high_14 = x_act_high_long[-14:]
x_rec_high_14 = x_rec_high_long[-14:]
x_det_high_14 = x_det_high_long[-14:]

x_conf_low_14 = x_conf_low_long[-14:]
x_act_low_14 = x_act_low_long[-14:]
x_rec_low_14 = x_rec_low_long[-14:]
x_det_low_14 = x_det_low_long[-14:]

x_conf_ls = []
x_act_ls = []
x_rec_ls = []
x_det_ls = []
dt = ['Tomorrow']

i = 0
for i in range(2, len(x_conf_high_14)+1):
    dt.append(str(int(i)))
                
i = 0
for i in range(len(x_conf_high_14)):
    x_conf_ls = np.append(x_conf_ls, str(x_conf_low_14[i]) + ' to ' + str(x_conf_high_14[i]))
    x_act_ls = np.append(x_act_ls, str(x_act_low_14[i]) + ' to ' + str(x_act_high_14[i]))
    x_rec_ls = np.append(x_rec_ls, str(x_rec_low_14[i]) + ' to ' + str(x_rec_high_14[i]))
    x_det_ls = np.append(x_det_ls, str(x_det_low_14[i]) + ' to ' + str(x_det_high_14[i]))
    

print()

print("conf_loss = {}".format(conf_loss))
print("rec_loss = {}".format(rec_loss))
print("det_loss = {}".format(det_loss))

print()

print("pred_conf = {}".format(pred_conf))
print("pred_rec = {}".format(pred_rec))
print("pred_det = {}".format(pred_det))

now = datetime.now()
date = now.strftime("%d-%m-%Y")

day14 = {'Day':dt, 'Confirmations':x_conf_ls, 'Active':x_act_ls, 'Recoveries':x_rec_ls, 'Deaths':x_det_ls}
df_day14 = pd.DataFrame(day14)
df_day14.to_html(os.path.join(dir_path, 'HTML', 'day14.html'), border=0, justify = 'left', index = False)


reports = {"date":date, "pred_conf":pred_conf, "pred_act":pred_act, "pred_rec":pred_rec, "pred_det":pred_det, "x_conf_long_pred":x_conf_ls[-1], "x_act_long_pred":x_act_ls[-1], "x_rec_long_pred":x_rec_ls[-1], "x_det_long_pred":x_det_ls[-1]}
df_reports = pd.DataFrame(reports, index=[0])
df_reports.to_csv(os.path.join(dir_path, 'CSV', 'REPORTS.csv'))