#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import os
import shutil
from datetime import datetime
import tensorflow as tf
import keras
import ftplib


# # State Data

# In[2]:


api_url_data = 'https://api.covid19india.org/data.json'
r_data = requests.get(api_url_data)
data_time_series = r_data.json()


# In[3]:





# In[4]:


state_data = data_time_series.get('statewise')


# In[5]:


state_list = []
confirmed_list = []
recovered_list = []
deaths_list = []

deltaconfirmed_list = []
deltarecovered_list = []
deltadeaths_list = []

lastupdatedtime_list = []


for j in range(len(state_data)):
    state = state_data[j].get('state')
    
    confirmed = state_data[j].get('confirmed')        
    recovered = state_data[j].get('recovered')
    deaths = state_data[j].get('deaths')
    
    deltaconfirmed = state_data[j].get('deltaconfirmed')
    deltarecovered = state_data[j].get('deltarecovered')
    deltadeaths = state_data[j].get('deltadeaths')
    
    lastupdatedtime = state_data[j].get('lastupdatedtime')
    
    
    if confirmed != '0':
        state_list.append(state)
        
        confirmed_list.append(confirmed)
        recovered_list.append(recovered)
        deaths_list.append(deaths)
        
        deltaconfirmed_list.append(deltaconfirmed)
        deltarecovered_list.append(deltarecovered)
        deltadeaths_list.append(deltadeaths)

        lastupdatedtime_list.append(lastupdatedtime)


# In[6]:


confirmed_list = np.array(confirmed_list, dtype = int)
recovered_list = np.array(recovered_list, dtype = int)
deaths_list = np.array(deaths_list, dtype = int)

active = np.subtract(confirmed_list, np.add(recovered_list, deaths_list))
death_rate = np.divide(deaths_list, confirmed_list)*100
recovery_rate = np.divide(recovered_list, confirmed_list)*100

death_rate_list = []
recovery_rate_list = []

for s in death_rate:
    s = round(s,1)
    death_rate_list = np.append(death_rate_list, s)
for p in recovery_rate:
    p = round(p,1)
    recovery_rate_list = np.append(recovery_rate_list, p)


# In[7]:


state_data = {'State':state_list[1:],'Confirmed':confirmed_list[1:], 'Active':active[1:], 'Recovered':recovered_list[1:], 'Deaths':deaths_list[1:], 'Recovery Rate(%)':recovery_rate_list[1:], 'Death Rate(%)':death_rate_list[1:], 'Last Updated':lastupdatedtime_list[1:]}
df_state_data = pd.DataFrame(state_data)
df_state_data.to_csv('State_data.csv')
df_state_data.to_html('State_data.html', border=0, justify = 'left', index = False, table_id = "state_data_table")


# # Case Time Plot:

# In[8]:


time = data_time_series.get('cases_time_series')


# In[9]:


date_list = []
dailyconfirmed_list = []
dailydeceased_list = []
dailyrecovered_list = []

totalconfirmed_list = []
totaldeceased_list = []
totalrecovered_list = []
t = 0
for t in range(len(time)):
    
    date = time[t].get('date')
    date_list.append(date)
    
    dailyconfirmed = time[t].get('dailyconfirmed')
    dailyconfirmed_list.append(dailyconfirmed)
    
    dailydeceased = time[t].get('dailydeceased')
    dailydeceased_list.append(dailydeceased)
    
    dailyrecovered = time[t].get('dailyrecovered')
    dailyrecovered_list.append(dailyrecovered)
    
    totalconfirmed = time[t].get('totalconfirmed')
    totalconfirmed_list.append(totalconfirmed)
    
    totalrecovered = time[t].get('totalrecovered')
    totalrecovered_list.append(totalrecovered)
    
    totaldeceased = time[t].get('totaldeceased')
    totaldeceased_list.append(totaldeceased)


# In[10]:


total_data = {'Confirmed':str(confirmed_list[0]) + ' (+' + str(deltaconfirmed_list[0]) + ')', 'Active':active[0], 'Recovered':str(recovered_list[0]) + ' (+' + str(deltarecovered_list[0]) + ')', 'Deaths':str(deaths_list[0]) + ' (+' + str(deltadeaths_list[0]) + ')', 'Recovery Rate(%)':recovery_rate_list[0], 'Death Rate(%)':death_rate_list[0]}
df_total_data = pd.DataFrame(total_data, index=[0])
df_total_data.to_csv('total_data.csv')
df_total_data.to_html('total_data.html', border=0, justify = 'center', index=False)


# In[11]:


day_range = 14

daily_data = {'Daily Confirmations':dailyconfirmed_list[-day_range:], 'Daily Recoveries':dailyrecovered_list[-day_range:], 'Daily Deaths':dailydeceased_list[-day_range:], 'Total Confirmations':totalconfirmed_list[-day_range:], 'Total Recoveries':totalrecovered_list[-day_range:], 'Total Deaths':totaldeceased_list[-day_range:]}
df_daily_data = pd.DataFrame(daily_data, index = [date_list[-day_range:]])
df_daily_data.to_csv('daily_data.csv')
df_daily_data.to_html('daily_data.html', border=0, justify = 'left')


# In[12]:


totalconfirmed_list = np.array(totalconfirmed_list, dtype=int)
totalrecovered_list = np.array(totalrecovered_list, dtype=int)
totaldeceased_list = np.array(totaldeceased_list, dtype=int)

dailyconfirmed_list = np.array(dailyconfirmed_list, dtype=int)
dailyrecovered_list = np.array(dailyrecovered_list, dtype=int)
dailydeceased_list = np.array(dailydeceased_list, dtype=int)



# # ICMR Reports

# In[29]:

tested = data_time_series.get('tested')

totalsamplestested_list = []
report_date_list = []

for i in range(len(tested)):
    report_date = tested[i].get('updatetimestamp')
    report_date = report_date[0:10]
    report_date_list.append(report_date)
    
    totalsamplestested = tested[i].get('totalsamplestested')
    totalsamplestested_list.append(totalsamplestested)

dt_list_total = report_date_list[-14:]
tst_list_total = np.array(totalsamplestested_list[-14:], dtype=int)

dt_list_daily = report_date_list[-14:-1]

i = 0
tst_list_daily = []
for i in range(len(tst_list_total)):
    tst_daily = tst_list_total[i] - tst_list_total[i-1]
    tst_list_daily.append(tst_daily)

tst_list_daily = np.array(tst_list_daily[1:])
cnf_list = totalconfirmed_list[-15:-1]

# # index.html

# In[43]:


date_list_chart = []
totalconfirmed_list_chart = []
totalrecovered_list_chart = []
totaldeceased_list_chart = []
dailyconfirmed_list_chart = []
dailyrecovered_list_chart = []
dailydeceased_list_chart = []

i,j,k,l,m,n,o = 0,0,0,0,0,0,0

for i in date_list:
    date_list_chart.append(i)
    
for j in totalconfirmed_list:
    totalconfirmed_list_chart.append(j)

for k in totalrecovered_list:
    totalrecovered_list_chart.append(k)
    
for l in totaldeceased_list:
    totaldeceased_list_chart.append(l)
    
for m in dailyconfirmed_list:
    dailyconfirmed_list_chart.append(m)
    
for n in dailyrecovered_list:
    dailyrecovered_list_chart.append(n)
    
for o in dailydeceased_list:
    dailydeceased_list_chart.append(o)


# In[44]:


now = datetime.now()
date = now.strftime("%d-%m-%Y")
date_time = now.strftime("%d-%m-%Y at %H:%M:%S")

index = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=0.77, shrink-to-fit=yes">
    <meta name="Description" content="Insights and Future Prediction of Covid-19 Pandemic in India">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>Insights of Covid-19 in India</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/v/bs4/dt-1.10.20/datatables.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <style>
      @import url('https://fonts.googleapis.com/css?family=Roboto+Slab&display=swap');
      *{font-family: 'Roboto Slab', serif}
    </style>
</head>
<body>

<nav class="navbar bg-light navbar-expand-sm navbar-light sticky-top">
    <a class="navbar-brand" href="index""><b>Insights of Covid-19</b> <i class="fas fa-virus"></i></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
                <a class="nav-link" href="index"><b>Home <i class="fas fa-home"></i></b></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="trendAnalysis"><b>Trend Analysis</b></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="futurePrediction"><b>Future Prediction</b></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="helpfulResources"><b>Helpful Resources</b></a>
            </li>
        </ul>
    </div>
</nav>

<div class="text-center">
    <br>
    <h1 class="text-center"><b>Insights of Covid-19 Pandemic in India</b></h1>
    <p class="text-center">
        Live information about Novel Corona Virus spread in India.
        <br>
        Check out the <a href="https://telegra.ph/Data-Sources-for-Covidtracker-indiaml-04-05" target="_blank" rel="noopener">data sources</a> for this website.
        <br>
        Last updated on """ + str(date_time) + """
        <br>
        <br>
        <br>
        <br>
    </p>
</div>

<div class="container">
    <div class="row justify-content-center">
        
        <div class="col-lg-4 col mb-3">
            <div class="card border-0">
                  <div class="text-primary">
                    <div class="card-body">
                      <h6 class="card-title"><b>Total <br> Confirmed</b></h6>
                      <h3 class="card-text"><b>""" + str(confirmed_list[0]) + """</b></h3>
                      <h6 class="card-text"> +""" + str(deltaconfirmed_list[0]) + """</h6>
                    </div>
                  </div>
            </div>
        </div>
    
        <div class="col-lg-8 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_3" width="400" height="150""></canvas>
            <script>
            var ctx_3 = document.getElementById('myChart_3').getContext('2d');
            var mixedChart_3 = new Chart(ctx_3, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Confirmations',
                        data: """ + str(dailyconfirmed_list_chart[-28:]) + """,
                        backgroundColor: [
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                            'rgba(0,0,255,0)',
                        ],
                    },{
                        label: '',
                        data: """ + str(dailyconfirmed_list_chart[-28:]) + """,
                        borderColor: "rgba(0,0,255,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-28:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-4 col mb-3">
            <div class="card border-0">
                  <div class="text-success">
                    <div class="card-body">
                      <h6 class="card-title"><b>Total <br> Recovered</b></h6>
                      <h3 class="card-text"><b>""" + str(recovered_list[0]) + """</b></h3>
                      <h6 class="card-text"> +""" + str(deltarecovered_list[0]) + """</h6>
                    </div>
                  </div>
            </div>
        </div>

        
        <div class="col-lg-8 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_31" width="400" height="150""></canvas>
            <script>
            var ctx_31 = document.getElementById('myChart_31').getContext('2d');
            var mixedChart_31 = new Chart(ctx_31, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Recoveries',
                        data: """ + str(dailyrecovered_list_chart[-28:]) + """,
                        backgroundColor: [
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                            'rgba(92,184,92,0)',
                        ],
                    },{
                        label: '',
                        data: """ + str(dailyrecovered_list_chart[-28:]) + """,
                        borderColor: "rgba(92,184,92,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-28:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-4 col mb-3">
            <div class="card border-0">
                  <div class="text-danger">
                    <div class="card-body">
                      <h6 class="card-title"><b>Total <br> Deceased</b></h6>
                      <h3 class="card-text"><b>""" + str(deaths_list[0]) + """</b></h3>
                      <h6 class="card-text"> +""" + str(deltadeaths_list[0]) + """</h6>
                    </div>
                  </div>
            </div>
        </div>
        
        <div class="col-lg-8 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_32" width="400" height="150""></canvas>
            <script>
            var ctx_32 = document.getElementById('myChart_32').getContext('2d');
            var mixedChart_32 = new Chart(ctx_32, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Deaths',
                        data: """ + str(dailydeceased_list_chart[-28:]) + """,
                        backgroundColor: [
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                            'rgba(255,0,0,0)',
                        ],
                    },{
                        label: '',
                        data: """ + str(dailydeceased_list_chart[-28:]) + """,
                        borderColor: "rgba(255,0,0,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-28:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Time'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>

        
    </div>
</div>

<br>
<br>

<div class="container">
    <div class="row justify-content-center">

        <div class="col-lg-6 col mb-3">
            <div class="card bg-success border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Recovery Rate</b></h4>
                      <p class="card-text"><b>""" + str(recovery_rate_list[0]) + '%' + """</b></p>
                    </div>
                  </div>
            </div>
        </div>


        <div class="col-lg-6 col mb-3">
            <div class="card bg-danger border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Death Rate</b></h4>
                      <p class="card-text"><b>""" + str(death_rate_list[0]) + '%' + """</b></p>
                    </div>
                  </div>
            </div>
        </div>
        
    </div>
</div>

<br>

<footer class="py-3">
    <div class="sticky-bottom">
        <div class="container">
            <div class="row justify-content-center">
                <p class="m-0 text-center text-dark">
                    Copyright <i class="fa fa-copyright"></i> 2020. Made with <i class="fa fa-heart"></i> by <a href="https://github.com/sudo-rajarshi" target="_blank" rel="noopener">Rajarshi Bhadra</a>
                </p>
            </div>
        </div>
    </div>
</footer>
</body>
</html>
"""

index_ = open("index.htm","w")
index_.write(index)
index_.close()

# # trend.html

# In[45]:


now = datetime.now()
date = now.strftime("%d-%m-%Y")
date_time = now.strftime("%d-%m-%Y at %H:%M:%S")

intro = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=0.77, shrink-to-fit=yes">
    <meta name="Description" content="Insights and Future Prediction of Covid-19 Pandemic in India">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>Insights of Covid'19 in India</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.4.1/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/v/bs4/dt-1.10.20/datatables.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <style>
      @import url('https://fonts.googleapis.com/css?family=Roboto+Slab&display=swap');
      *{font-family: 'Roboto Slab', serif}
    </style>
</head>
<body>

<nav class="navbar bg-light navbar-expand-sm navbar-light sticky-top">
    <a class="navbar-brand" href="index""><b>Insights of Covid-19</b> <i class="fas fa-virus"></i></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item">
                <a class="nav-link" href="index"><b>Home</b></a>
            </li>
            <li class="nav-item active">
                <a class="nav-link" href="trendAnalysis"><b>Trend Analysis <i class="fas fa-chart-line"></i></b></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="futurePrediction"><b>Future Prediction</b></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="helpfulResources"><b>Helpful Resources</b></a>
            </li>
        </ul>
    </div>
</nav>

<br>

<div class="text-center">
    <h3 class="text-center"><b>Trend Analysis of Corona Virus Spread</b></h3>
    <p class="text-center">
        Last updated on """ + str(date_time) + """
    </p>
</div>


<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-3 col mb-3">
            <div class="card bg-primary border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Confirmed</b></h4>
                      <p class="card-text">""" + str(confirmed_list[0]) + ' (+' + str(deltaconfirmed_list[0]) + ')' + """</p>
                    </div>
                  </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-danger border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Active</b></h4>
                      <p class="card-text">""" + str(active[0]) + """</p>
                    </div>
                  </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-success border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Recovered</b></h4>
                      <p class="card-text">""" + str(recovered_list[0]) + ' (+' + str(deltarecovered_list[0]) + ')' + """</p>
                    </div>
                  </div>
            </div>
        </div>


        <div class="col-lg-3 col mb-3">
            <div class="card bg-dark border-0">
                  <div class="text-white">
                    <div class="card-body">
                      <h4 class="card-title"><b>Deceased</b></h4>
                      <p class="card-text">""" + str(deaths_list[0]) + ' (+' + str(deltadeaths_list[0]) + ')' + """</p>
                    </div>
                  </div>
            </div>
        </div>
    </div>
</div>


<br>
<br>
<h3 class="text-center">
    <b>Analysing Corona Virus spread in Different States</b>
</h3>

<br>
<div class="text-center">
  <input type="text" name="" id="state_data_search" placeholder=" Search by State" onkeyup="search()">
</div>
<br>

<div class="container mb-3">
<div class="table-responsive">
"""

intro_ = open("trend_intro.html","w")
intro_.write(intro)
intro_.close()

# In[46]:


confirmed_list_chart = []

i = 0
for i in confirmed_list:
    confirmed_list_chart.append(i)


# In[48]:


daily_data_intro = """
</div>
</div>

<script>
  const search = () =>{
    let filter = document.getElementById('state_data_search').value.toUpperCase();
    let resources_table = document.getElementById('state_data_table');
    let tr = resources_table.getElementsByTagName('tr');
    for(var i=0; i<tr.length; i++){
      let td = tr[i].getElementsByTagName('td')[0];
      if(td){
        let textvalue = td.textContent || td.innerHTML;
        if(textvalue.toUpperCase().indexOf(filter) > -1){
          tr[i].style.display = "";
        }
        else{
          tr[i].style.display = "none";
        }
        }
      }
    }
</script>

<br>
<br>

<h3 class="text-center">
    <b>Trend analysis of Corona Virus spread using the data of last 14 days</b>
</h3>

<div class="container mb-3">
<div class="table-responsive">
"""

daily_data_intro_ = open('daily_data_intro.html', 'w')
daily_data_intro_.write(daily_data_intro)
daily_data_intro_.close()


# In[49]:


chart_total = """
</div>
</div>

<br>
<br>

<h3 class="text-center">
    <b>Analysis of last 42 days</b>
</h3>

<br>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_3"></canvas>
            <script>
            var ctx_3 = document.getElementById('myChart_3').getContext('2d');
            var mixedChart_3 = new Chart(ctx_3, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Confirmations',
                        data: """ + str(totalconfirmed_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(totalconfirmed_list_chart[-42:]) + """,
                        borderColor: "rgba(0,0,255,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_4"></canvas>
            <script>
            var ctx_4 = document.getElementById('myChart_4').getContext('2d');
            var mixedChart_4 = new Chart(ctx_4, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Confirmations',
                        data: """ + str(dailyconfirmed_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                            "rgba(0,0,255,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(dailyconfirmed_list_chart[-42:]) + """,
                        borderColor: "rgba(0,0,255,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_31"></canvas>
            <script>
            var ctx_31 = document.getElementById('myChart_31').getContext('2d');
            var mixedChart_31 = new Chart(ctx_31, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Recoveries',
                        data: """ + str(totalrecovered_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(totalrecovered_list_chart[-42:]) + """,
                        borderColor: "rgba(92,184,92,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_41"></canvas>
            <script>
            var ctx_41 = document.getElementById('myChart_41').getContext('2d');
            var mixedChart_41 = new Chart(ctx_41, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Recoveries',
                        data: """ + str(dailyrecovered_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                                "rgba(92,184,92,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(dailyrecovered_list_chart[-42:]) + """,
                        borderColor: "rgba(92,184,92,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_32"></canvas>
            <script>
            var ctx_32 = document.getElementById('myChart_32').getContext('2d');
            var mixedChart_32 = new Chart(ctx_32, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Deaths',
                        data: """ + str(totaldeceased_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(totaldeceased_list_chart[-42:]) + """,
                        borderColor: "rgba(255,0,0,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_42"></canvas>
            <script>
            var ctx_42 = document.getElementById('myChart_42').getContext('2d');
            var mixedChart_42 = new Chart(ctx_42, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Deaths',
                        data: """ + str(dailydeceased_list_chart[-42:]) + """,
                        barPercentage: 0.7,
                        backgroundColor: [
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                                "rgba(255,0,0,1)",
                        ],
                    },{
                        label: '',
                        data: """ + str(dailydeceased_list_chart[-42:]) + """,
                        borderColor: "rgba(255,0,0,1)",
                        type: 'line',
                        fill: false,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-42:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            gridLines: {
                                drawOnChartArea: false
                            },
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                        },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }
            });
            </script>
        </div>
    </div>
</div>
<br>
"""

chart_total_ = open("chart_total.html","w")
chart_total_.write(chart_total)
chart_total_.close()


ICMR_report_data_intro = """
</div>
</div>

<br>

<h3 class="text-center">
    <b>Test data of last 14 days from ICMR</b>
</h3>

<div class="container mb-3">
<div class="table-responsive">
"""

ICMR_report_data_intro_ = open('ICMR_report_data_intro.html', 'w')
ICMR_report_data_intro_.write(ICMR_report_data_intro)
ICMR_report_data_intro_.close()

report_date_list_chart = []
totalsamplestested_list_chart = []
dt_list_daily_chart = []
totalsamplestested_daily_list_chart = []

i,j,k,l = 0,0,0,0

    
for i in tst_list_total:
    totalsamplestested_list_chart.append(i)
    
for j in dt_list_total:
    j = j[:-5]
    report_date_list_chart.append(j)
    
for k in dt_list_daily:
    k = k[:-5]
    dt_list_daily_chart.append(k)
    
for l in tst_list_daily:
    totalsamplestested_daily_list_chart.append(l)

icmr_stat_sample = """
</div>
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_1"></canvas>
            <script>
            var ctx_1 = document.getElementById('myChart_1').getContext('2d');
            var mixedChart_1 = new Chart(ctx_1, {
                type: 'bar',
                data: {
                    labels: """ + str(report_date_list_chart) + """,
                    datasets: [{
                        label: 'Total Samples Tested',
                        data: """ + str(totalsamplestested_list_chart) + """,
                        borderColor: [
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                        ],
                        backgroundColor: [
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                        ],
                        borderWidth: 1,
                        fill: true
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                            },
                            gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }

            });
            </script>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <canvas id="myChart_12"></canvas>
            <script>
            var ctx_12 = document.getElementById('myChart_12').getContext('2d');
            var mixedChart_12 = new Chart(ctx_12, {
                type: 'bar',
                data: {
                    labels: """ + str(dt_list_daily_chart) + """,
                    datasets: [{
                        label: 'Daily Samples Tested',
                        data: """ + str(totalsamplestested_daily_list_chart) + """,
                        borderColor: [
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                            'rgba(255,0,0,1)',
                        ],
                        backgroundColor: [
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                            'rgba(255, 0, 0, 0.3)',
                        ],
                        borderWidth: 1,
                        fill: true
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: 'Dates'
                            },
                            gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }],
                        yAxes: [{
                             gridLines: {
                                drawOnChartArea: false
                            },
                            ticks: {
                                display: false
                            }
                        }]
                    }
                }

            });
            </script>
        </div>
    </div>
</div>
"""

icmr_stat_sample_ = open("icmr_stat_sample.html","w")
icmr_stat_sample_.write(icmr_stat_sample)
icmr_stat_sample_.close()

footer = """
<footer class="py-3">
    <div class="sticky-bottom">
        <div class="container">
            <div class="row justify-content-center">
                <p class="m-0 text-center text-dark">
                    Copyright <i class="fa fa-copyright"></i> 2020. Made with <i class="fa fa-heart"></i> by <a href="https://github.com/sudo-rajarshi" target="_blank" rel="noopener">Rajarshi Bhadra</a>
                </p>
            </div>
        </div>
    </div>
</footer>
</body>
</html>
"""

footer_ = open("footer.html","w")
footer_.write(footer)
footer_.close()


# In[56]:


with open('trend_intro.html') as rd: 
    intro = rd.read()
    
with open('State_data.html') as rd:
    state_wise = rd.read()
    state_wise = state_wise[:25] + "table table-striped table-bordered table-sm text-left " + state_wise[:35] + str(' align="left"') + state_wise[35:]
    state_wise = state_wise[:159] + ' class="thead-dark"' + state_wise[159:]
    
with open('daily_data_intro.html') as rd: 
    daily_intro = rd.read()
    
with open('ICMR_report_data_intro.html') as rd: 
    ICMR_intro = rd.read()
    
with open('icmr_stat_sample.html') as rd: 
    ICMR_chart = rd.read()
    
with open('daily_data.html') as rd: 
    daily = rd.read()
    daily = daily[:25] + "table table-striped table-bordered table-sm text-left " + daily[:35] + str(' align="left"') + daily[35:]
    daily = daily[:137] + ' class="thead-dark"' + daily[137:]
    
with open('chart_total.html') as rd: 
    line_chart_total = rd.read()
    
with open('footer.html') as rd: 
    footer = rd.read()
    
data = intro + state_wise + ICMR_intro + ICMR_chart + daily_intro + daily + line_chart_total + footer

with open ('trendAnalysis.htm', 'w') as fp: 
    fp.write(data) 

