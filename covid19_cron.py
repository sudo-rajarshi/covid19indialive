import pandas as pd
import numpy as np
import requests
from datetime import datetime
import ftplib
import time as ts


# # State Data
api_url_data = 'https://api.covid19india.org/data.json'

r_data = requests.get(api_url_data)
data_time_series = r_data.json()
state_data = data_time_series.get('statewise')

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

confirmed_list_ = []
recovered_list_ = []
deaths_list_ = []

# i = 0
# for i in range(len(confirmed_list)):
#     confirmed_list_ = np.append(confirmed_list_, str(confirmed_list[i]))
#     recovered_list_ = np.append(recovered_list_, str(recovered_list[i]))
#     deaths_list_ = np.append(deaths_list_, str(deaths_list[i]))
    
i = 0
for i in range(len(confirmed_list)):
    confirmed_list_ = np.append(confirmed_list_, """<b>""" + str(confirmed_list[i]) + """</b> <br><i class="fas fa-arrow-up"></i> """ + str(deltaconfirmed_list[i]))
    recovered_list_ = np.append(recovered_list_, """<b>""" + str(recovered_list[i]) + """</b> <br><i class="fas fa-arrow-up"></i> """ + str(deltarecovered_list[i]))
    deaths_list_ = np.append(deaths_list_, """<b>""" + str(deaths_list[i]) + """</b> <br><i class="fas fa-arrow-up"></i> """ + str(deltadeaths_list[i]))


state_data = {'State':state_list[1:],'Confirmed':confirmed_list_[1:], 'Active':active[1:], 'Recovered':recovered_list_[1:], 'Deaths':deaths_list_[1:], 'Recovery(%)':recovery_rate_list[1:], 'Death(%)':death_rate_list[1:], 'Updated':lastupdatedtime_list[1:]}
df_state_data = pd.DataFrame(state_data)
df_state_data.to_csv('/home/rajarshi/Documents/Projects/COVIDTRACKER/State_data.csv')
df_state_data.to_html('/home/rajarshi/Documents/Projects/COVIDTRACKER/State_data.html', border=0, justify = 'left', index = False, table_id = "state_data_table", escape=False)

with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/State_data.html') as rd:
    state_wise = rd.read()
    state_wise = state_wise[:25] + "table table-striped table-bordered table-sm text-left " + state_wise[:35] + str(' align="left"') + state_wise[35:]
    state_wise = state_wise[:159] + ' class="thead-dark"' + state_wise[159:]


# # Case Time Plot:
time = data_time_series.get('cases_time_series')

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

day_range = 14

daily_data = {'Daily Confirmations':dailyconfirmed_list[-day_range:], 'Daily Recoveries':dailyrecovered_list[-day_range:], 'Daily Deaths':dailydeceased_list[-day_range:], 'Total Confirmations':totalconfirmed_list[-day_range:], 'Total Recoveries':totalrecovered_list[-day_range:], 'Total Deaths':totaldeceased_list[-day_range:]}
df_daily_data = pd.DataFrame(daily_data, index = [date_list[-day_range:]])
df_daily_data.to_csv('/home/rajarshi/Documents/Projects/COVIDTRACKER/daily_data.csv')
df_daily_data.to_html('/home/rajarshi/Documents/Projects/COVIDTRACKER/daily_data.html', border=0, justify = 'left')

with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/daily_data.html') as rd: 
    daily = rd.read()
    daily = daily[:25] + "table table-striped table-bordered table-sm text-left " + daily[:35] + str(' align="left"') + daily[35:]
    daily = daily[:137] + ' class="thead-dark"' + daily[137:]

totalconfirmed_list = np.array(totalconfirmed_list, dtype=int)
totalrecovered_list = np.array(totalrecovered_list, dtype=int)
totaldeceased_list = np.array(totaldeceased_list, dtype=int)

dailyconfirmed_list = np.array(dailyconfirmed_list, dtype=int)
dailyrecovered_list = np.array(dailyrecovered_list, dtype=int)
dailydeceased_list = np.array(dailydeceased_list, dtype=int)



# # ICMR Reports
tested = data_time_series.get('tested')

totalsamplestested_list = []
report_date_list = []

for i in range(len(tested)):
    report_date = tested[i].get('updatetimestamp')
    report_date = report_date[0:10]
    report_date_list.append(report_date)
    
    totalsamplestested = tested[i].get('totalsamplestested')
    totalsamplestested_list.append(totalsamplestested)

dt_list_total = report_date_list[-28:]
tst_list_total = np.array(totalsamplestested_list[-28:], dtype=int)

dt_list_daily = report_date_list[-28:-1]

i = 0
tst_list_daily = []
for i in range(len(tst_list_total)):
    tst_daily = tst_list_total[i] - tst_list_total[i-1]
    tst_list_daily.append(tst_daily)

tst_list_daily = np.array(tst_list_daily[1:])
cnf_list = totalconfirmed_list[-29:-1]

conf_rate = str(totalconfirmed_list[-1] / tst_list_total[-1]*100)
conf_rate = conf_rate[:1]

report_date_list_chart = []
totalsamplestested_list_chart = []
dt_list_daily_chart = []
totalsamplestested_daily_list_chart = []

i,j,k,l = 0,0,0,0
    
for i in tst_list_total:
    totalsamplestested_list_chart.append(i)
    
for j in dt_list_total:
    report_date_list_chart.append(j)
    
for k in dt_list_daily:
    dt_list_daily_chart.append(k)
    
for l in tst_list_daily:
    totalsamplestested_daily_list_chart.append(l)


# # index.html
date_list_chart = []
totalconfirmed_list_chart = []
totalrecovered_list_chart = []
totaldeceased_list_chart = []
dailyconfirmed_list_chart = []
dailyrecovered_list_chart = []
dailydeceased_list_chart = []

population = 1352600000

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

per_mil_test = int(totalsamplestested_list_chart[-1]/population*1000000)
per_mil_conf = int(((totalconfirmed_list[-1] / tst_list_total[-1]*100)*per_mil_test)/100)
per_mil_rec = int((recovery_rate_list[0]*per_mil_conf)/100)
per_mil_det = int((death_rate_list[0]*per_mil_conf)/100)

reports = pd.read_csv('/home/rajarshi/Documents/Projects/COVIDTRACKER/REPORTS.csv')

x_conf_long_pred = reports['pred_conf'].values[0]
x_act_long_pred = reports['pred_act'].values[0]
x_rec_long_pred = reports['pred_rec'].values[0]
x_det_long_pred = reports['pred_det'].values[0]

date_pred = reports['date'].values

state_list[state_list.index('Uttarakhand')]='IN-UT'
state_list[state_list.index('Odisha')]='Orissa'

sss = []
sss = [['State', 'Confirmed Cases', 'Recovered Cases']]

for jj in range(len(state_list)):
    sss.append([state_list[jj], confirmed_list[jj], recovered_list[jj]])
sss.pop(1)

time = data_time_series.get('cases_time_series')

with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/day14.html') as rd: 
    pred_day14 = rd.read()
    pred_day14 = pred_day14[:25] + "table table-striped table-bordered table-sm text-left " + pred_day14[:35] + str(' align="left"') + pred_day14[35:]
    pred_day14 = pred_day14[:137] + ' class="thead-dark"' + pred_day14[137:]


now = datetime.now()
date = now.strftime("%d-%m-%Y")
date_time = now.strftime("%d-%m-%Y at %H:%M")

index = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-168253703-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'UA-168253703-1');
    </script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=0.77, shrink-to-fit=yes">
    <meta name="Description" content="Insights and Future Prediction of Covid-19 Pandemic in India. Get Detailed Analysis of the spread of the virus in India.">
    <meta name="keywords" content="coronavirus, corona, covid, covid19, covid-19, covidindia, covid-19 india, covid-19 india tracker, india, virus, pandemic, world">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <meta name="cf-2fa-verify" content="e85e8a45e5ef19b">
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
                <a class="nav-link" href="helpfulResources"><b>Helpful Resources</b></a>
            </li>
        </ul>
    </div>
</nav>

<div class="text-center">
    <br>
    <h1 class="text-center"><b>Insights of Covid-19 Pandemic in India</b></h1>
    <p class="text-center">
        Live information about Novel Corona Virus spread in India
        <br>
        Check out the <a href="https://telegra.ph/Data-Sources-for-Covidtracker-indiaml-04-05" target="_blank" rel="noopener">data sources</a> for this website
    </p>
    
</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-6 col mb-3">
            <script src="https://www.gstatic.com/charts/loader.js"></script>
                <script>
                google.charts.load('current', {
                    'packages':['geochart'],
                    'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
                });
                google.charts.setOnLoadCallback(drawRegionsMap);

                function drawRegionsMap() {
                    var data = google.visualization.arrayToDataTable(""" + str(sss) + """);

                    var options = {
                        region: 'IN',
                        displayMode: 'regions',
                        resolution: 'provinces',
                        datalessRegionColor: '#ffffff'
                    };

                    var chart = new google.visualization.GeoChart(document.getElementById('geochart-colors'));
                    chart.draw(data, options);
                };
                </script>
            <div id="geochart-colors" align="center"></div>
            </div>
        </div>
    </div>
</div>


<div class="container">
    <div class="row justify-content-center">

        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-primary">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Total <br> Confirmed</b></h6>
                            <h4 class="card-text"><b>""" + str(confirmed_list[0]) + """</b></h4>
                            <h6 class="card-text"> +""" + str(deltaconfirmed_list[0]) + """</h6>
                        </div>
                    </div>
                    </div>
            </div>
        </div>

        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-success">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Total <br> Recovered</b></h6>
                            <h4 class="card-text"><b>""" + str(recovered_list[0]) + """</b></h4>
                            <h6 class="card-text"> +""" + str(deltarecovered_list[0]) + """</h6>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-dark">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Total <br> Deceased</b></h6>
                            <h4 class="card-text"><b>""" + str(deaths_list[0]) + """</b></h4>
                            <h6 class="card-text"> +""" + str(deltadeaths_list[0]) + """</h6>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-primary">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Confirmation <br> Rate</b></h6>
                            <h4 class="card-text"><b>""" + conf_rate + '%' + """</b></h4>
                            <a data-toggle="tooltip" data-placement="bottom" title='Out of 100 tests """+ conf_rate  +""" people have tested positive'>
                                <i class="fas fa-question-circle"></i>
                            </a>
                        </div>
                    </div>
                    </div>
            </div>
        </div>

        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-success">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Recovery <br> Rate</b></h6>
                            <h4 class="card-text"><b>""" + str(int(recovery_rate_list[0])) + '%' + """</b></h4>
                            <a data-toggle="tooltip" data-placement="top" title='Out of 100 confirmed cases """+ str(int(recovery_rate_list[0]))  +""" people have recovered'>
                                <i class="fas fa-question-circle"></i>
                            </a>
                        </div>
                    </div>
                    </div>
            </div>
        </div>
        
        <div class="col-lg-2 col mb-3">
            <div class="card border-0">
                    <div class="text-dark">
                    <div class="card-body">
                        <div class="text-center">
                            <h6 class="card-title"><b>Mortality <br> Rate</b></h6>
                            <h4 class="card-text"><b>""" + str(int(death_rate_list[0])) + '%' + """</b></h4>
                            <a data-toggle="tooltip" data-placement="bottom" title='Out of 100 confirmed cases """+ str(int(death_rate_list[0]))  +""" people have died'>
                                <i class="fas fa-question-circle"></i>
                            </a>
                        </div>
                    </div>
                    </div>
            </div>
        </div>

        <script>
            $('a[data-toggle="tooltip"]').tooltip({
                animated: 'fade',
                trigger: 'click'
            });
        </script>

        <div class="text-center">
            <a href="trendAnalysis" class="btn btn-warning" role="button" aria-pressed="true">
                <i class="text-center fas fa-chart-line fa-1x"></i> Trend of the Spread <i class="fas fa-external-link-square-alt"></i>
            </a>
        </div>

    </div>
</div>

<br>

<h4 class="text-center">
    <b>Spread per million people</b>
</h4>

<p class="text-center">
    Testing, confirmations, recoveries and deaths per million people
</p>

        
<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-6 col mb-3">
            <div class="card bg-info border-0">
                <div class="text-white">
                    <div class="card-body">
                        <div class="text-left">
                            <h5 class="card-title"><b>Samples Testing</b></h5>
                            <p class="card-text">Out of 1 million people <b>""" + str(per_mil_test) + """</b> people have been tested</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <div class="card bg-primary border-0">
                <div class="text-white">
                    <div class="card-body">
                        <div class="text-left">
                            <h5 class="card-title"><b>Confirmations</b></h5>
                            <p class="card-text">Out of """ + str(per_mil_test) + """ tests <b>""" + str(per_mil_conf) + """</b> people have been tested positive</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>
        
<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-6 col mb-3">
            <div class="card bg-success border-0">
                <div class="text-white">
                    <div class="card-body">
                        <div class="text-left">
                            <h5 class="card-title"><b>Recoveries</b></h5>
                            <p class="card-text">Out of """ + str(per_mil_conf) + """ positive cases <b>""" + str(per_mil_rec) + """</b> people have been recovered</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <div class="card bg-dark border-0">
                <div class="text-white">
                    <div class="card-body">
                        <div class="text-left">
                            <h5 class="card-title"><b>Deaths</b></h5>
                            <p class="card-text">Out of """ + str(per_mil_conf) + """ positive cases <b>""" + str(per_mil_det) + """</b> people have been deceased</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-8 col mb-3">
            <div class="card border-0">
                <div class="text-dark">
                    <div class="card-body">
                        <div class="text-center">
                            <h4 class="card-title"><b>Detailed Analysis of Different States</b></h4>
                            <p class="card-text">Get detailed analytics of confirmations, recoveries and deaths across different states</p>
                            <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#state" aria-expanded="false" aria-controls="state">
                                State Data <i class="fas fa-chevron-circle-down fa-1x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="collapse" id="state">

    <div class="text-center">
    <input type="text" name="" id="state_data_search" placeholder=" Search by State" onkeyup="search()">
    </div>
    <br>

<div class="container mb-3">
<div class="table-responsive">
""" + state_wise +"""
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

</div>

<h4 class="text-center">
    <b>Predictions of """ + date_pred[0] + """ using AI</b>
</h4>

<p class='text-center'>
    The following predictions are made by considering the current situation doesnot change with respect to time.
</p>

<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-3 col mb-3">
            <div class="card bg-primary border-0">
                <div class="text-white">
                    <div class="card-header">Today's Predictions</div>
                    <div class="card-body">
                    <h4 class="card-title"><b>Confirmation</b></h4>
                    <p class="card-text">""" + str(x_conf_long_pred) + """</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-3 col mb-3">
            <div class="card bg-danger border-0">
                <div class="text-white">
                    <div class="card-header">Today's Predictions</div>
                    <div class="card-body">             
                    <h4 class="card-title"><b>Active</b></h4>
                    <p class="card-text">""" + str(x_act_long_pred) + """</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-success border-0">
                <div class="text-white">
                    <div class="card-header">Today's Predictions</div>
                    <div class="card-body">             
                    <h4 class="card-title"><b>Recovery</b></h4>
                    <p class="card-text">""" + str(x_rec_long_pred) + """</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-dark border-0">
                <div class="text-white">
                    <div class="card-header">Today's Predictions</div>
                    <div class="card-body">
                    <h4 class="card-title"><b>Death</b></h4>
                    <p class="card-text">""" + str(x_det_long_pred) + """</p>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-8 col mb-3">
            <div class="card border-0">
                <div class="text-dark">
                    <div class="card-body">
                        <div class="text-center">
                            <p class="card-text">Get detailed Predictions of confirmations, recoveries and deaths for next 14 days</p>
                            <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#pred" aria-expanded="false" aria-controls="pred">
                                Predictions of each day for next 14 days <i class="fas fa-chevron-circle-down fa-1x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="collapse" id="pred">
<div class="container mb-3">
<div class="table-responsive">
""" + pred_day14 + """
</div>
</div>
</div>

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

index_ = open("/home/rajarshi/Documents/Projects/COVIDTRACKER/index.htm","w")
index_.write(index)
index_.close()


# # trend.html

now = datetime.now()
date = now.strftime("%d-%m-%Y")
date_time = now.strftime("%d-%m-%Y at %H:%M:%S")

intro = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-168253703-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'UA-168253703-1');
    </script>

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
                <a class="nav-link" href="helpfulResources"><b>Helpful Resources</b></a>
            </li>
        </ul>
    </div>
</nav>

<br>

<div class="text-center">
    <h4 class="text-center"><b>Today's Current Status</b></h4>
    <br>
</div>

<div class="container">
    <div class="row justify-content-center">
    
        <div class="col-lg-3 col mb-3">
            <div class="card bg-primary border-0">
                    <div class="text-white">
                    <div class="card-body">
                        <h3 class="card-title"><b>Confirmed</b></h3>
                        <p class="card-text">""" + str(confirmed_list[0]) + ' (+' + str(deltaconfirmed_list[0]) + ')' + """</p>
                    </div>
                    </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-danger border-0">
                    <div class="text-white">
                    <div class="card-body">
                        <h3 class="card-title"><b>Active</b></h3>
                        <p class="card-text">""" + str(active[0]) + """</p>
                    </div>
                    </div>
            </div>
        </div>

        <div class="col-lg-3 col mb-3">
            <div class="card bg-success border-0">
                    <div class="text-white">
                    <div class="card-body">
                        <h3 class="card-title"><b>Recovered</b></h3>
                        <p class="card-text">""" + str(recovered_list[0]) + ' (+' + str(deltarecovered_list[0]) + ')' + """</p>
                    </div>
                    </div>
            </div>
        </div>


        <div class="col-lg-3 col mb-3">
            <div class="card bg-dark border-0">
                    <div class="text-white">
                    <div class="card-body">
                        <h3 class="card-title"><b>Deceased</b></h3>
                        <p class="card-text">""" + str(deaths_list[0]) + ' (+' + str(deltadeaths_list[0]) + ')' + """</p>
                    </div>
                    </div>
            </div>
        </div>
    </div>
</div>
"""

intro_ = open("/home/rajarshi/Documents/Projects/COVIDTRACKER/trend_intro.html","w")
intro_.write(intro)
intro_.close()


confirmed_list_chart = []

i = 0
for i in confirmed_list:
    confirmed_list_chart.append(i)



daily_data_intro = """
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-8 col mb-3">
            <div class="card border-0">
                <div class="text-dark">
                    <div class="card-body">
                        <div class="text-center">
                            <h4 class="card-title"><b>In depth Trend Analysis of last 14 days</b></h4>
                            <p class="card-text">Detailed daily analysis of Confirmations, Recoveries and Deaths of last 14 days</p>
                            <button class="btn btn-warning" type="button" data-toggle="collapse" data-target="#trend" aria-expanded="false" aria-controls="state">
                                Trend Analysis <i class="fas fa-chevron-circle-down fa-1x"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="collapse" id="trend">
<div class="container mb-3">
<div class="table-responsive">
"""+ daily +"""
</div>
</div>
</div>
"""

daily_data_intro_ = open('/home/rajarshi/Documents/Projects/COVIDTRACKER/daily_data_intro.html', 'w')
daily_data_intro_.write(daily_data_intro)
daily_data_intro_.close()




chart_total = """
</div>
</div>

<h4 class="text-center">
    <b>Overall Analysis of last 56 days</b>
</h4>

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
                        label: 'Daily Confirmations',
                        data: """ + str(dailyconfirmed_list_chart[-56:]) + """,
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
                        data: """ + str(dailyconfirmed_list_chart[-56:]) + """,
                        pointRadius: 0,
                        borderColor: "rgba(0,0,255,1)",
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }
            });
            </script>
        </div>

        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_4"></canvas>
            <script>
            var ctx_4 = document.getElementById('myChart_4').getContext('2d');
            var mixedChart_4 = new Chart(ctx_4, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Confirmations',
                        data: """ + str(totalconfirmed_list_chart[-56:]) + """,
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
                        data: """ + str(totalconfirmed_list_chart[-56:]) + """,
                        pointRadius: 0,
                        borderColor: "rgba(0,0,255,1)",
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }
            });
            </script>
        </div>

        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_41"></canvas>
            <script>
            var ctx_41 = document.getElementById('myChart_41').getContext('2d');
            var mixedChart_41 = new Chart(ctx_41, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Recoveries',
                        data: """ + str(dailyrecovered_list_chart[-56:]) + """,
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
                        data: """ + str(dailyrecovered_list_chart[-56:]) + """,
                        borderColor: "rgba(92,184,92,1)",
                        pointRadius: 0,
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }
            });
            </script>
        </div>

        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_31"></canvas>
            <script>
            var ctx_31 = document.getElementById('myChart_31').getContext('2d');
            var mixedChart_31 = new Chart(ctx_31, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Recoveries',
                        data: """ + str(totalrecovered_list_chart[-56:]) + """,
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
                        data: """ + str(totalrecovered_list_chart[-56:]) + """,
                        borderColor: "rgba(92,184,92,1)",
                        pointRadius: 0,
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }
            });
            </script>
        </div>

        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_32"></canvas>
            <script>
            var ctx_32 = document.getElementById('myChart_32').getContext('2d');
            var mixedChart_32 = new Chart(ctx_32, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Daily Deaths',
                        data: """ + str(dailydeceased_list_chart[-56:]) + """,
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
                        data: """ + str(dailydeceased_list_chart[-56:]) + """,
                        borderColor: "rgba(255,0,0,1)",
                        pointRadius: 0,
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }
            });
            </script>
        </div>

        <div class="col-lg-6 col mb-3">
            <script src="https://cdn.jsdelivr.net/npm/chart.js@2.9.3/dist/Chart.min.js"></script>
            <canvas id="myChart_42"></canvas>
            <script>
            var ctx_42 = document.getElementById('myChart_42').getContext('2d');
            var mixedChart_42 = new Chart(ctx_42, {
                type: 'bar',
                data: {
                    datasets: [{
                        label: 'Total Deaths',
                        data: """ + str(totaldeceased_list_chart[-56:]) + """,
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
                        data: """ + str(totaldeceased_list_chart[-56:]) + """,
                        borderColor: "rgba(255,0,0,1)",
                        pointRadius: 0,
                        type: 'line',
                        fill: true,
                        order: 1
                    }],
                    labels: """ + str(date_list_chart[-56:]) + """
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
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

chart_total_ = open("/home/rajarshi/Documents/Projects/COVIDTRACKER/chart_total.html","w")
chart_total_.write(chart_total)
chart_total_.close()


ICMR_report_data_intro = """
</div>
</div>

<br>

<h4 class="text-center">
    <b>Test data of last 28 days from ICMR</b>
</h4>
"""

ICMR_report_data_intro_ = open('/home/rajarshi/Documents/Projects/COVIDTRACKER/ICMR_report_data_intro.html', 'w')
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
    report_date_list_chart.append(j)
    
for k in dt_list_daily:
    dt_list_daily_chart.append(k)
    
for l in tst_list_daily:
    totalsamplestested_daily_list_chart.append(l)

icmr_stat_sample = """
<div class="container">
    <div class="row justify-content-center">
        
        <div class="col-lg-6 col mb-3">
            <div class="card border-0">
                <div class="text-info">
                    <div class="text-center">
                        <div class="card-body">
                            <h5 class="card-title"><b>Tests per Million</b></h5>
                            <p class="card-text">""" + str(int((totalsamplestested_list_chart[-1]/population)*1000000)) + """</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-6 col mb-3">
            <div class="card border-0">
                <div class="text-info">
                    <div class="text-center">
                        <div class="card-body">
                            <h5 class="card-title"><b>Samples Tested</b></h5>
                            <p class="card-text">""" + str(totalsamplestested_list_chart[-1]) + """</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </div>
</div>

<div class="container">
    <div class="row justify-content-center">
    
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
                        borderWidth: 2,
                        fill: true
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }

            });
            </script>
        </div>

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
                        backgroundColor: [
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                            'rgba(255, 0, 0, 0)',
                        ],
                        borderWidth: 0,
                        fill: true
                    },{
                        label: '',
                        data: """ + str(totalsamplestested_list_chart) + """,
                        borderColor: "rgba(255,0,0,1)",
                        pointRadius: 0,
                        type: 'line',
                        fill: true,
                        order: 1
                    }]
                },
                options: {
                    scales: {
                        xAxes: [{
                            display: false
                        }],
                        yAxes: [{
                            display: false
                        }]
                    }
                }

            });
            </script>
        </div>
    </div>
</div>
"""

icmr_stat_sample_ = open("/home/rajarshi/Documents/Projects/COVIDTRACKER/icmr_stat_sample.html","w")
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

footer_ = open("/home/rajarshi/Documents/Projects/COVIDTRACKER/footer.html","w")
footer_.write(footer)
footer_.close()



with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/trend_intro.html') as rd: 
    intro = rd.read()
    
with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/daily_data_intro.html') as rd: 
    daily_intro = rd.read()
    
with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/ICMR_report_data_intro.html') as rd: 
    ICMR_intro = rd.read()
    
with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/icmr_stat_sample.html') as rd: 
    ICMR_chart = rd.read()
    
with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/chart_total.html') as rd: 
    line_chart_total = rd.read()
    
with open('/home/rajarshi/Documents/Projects/COVIDTRACKER/footer.html') as rd: 
    footer = rd.read()
    
data = intro + ICMR_intro + ICMR_chart + daily_intro + line_chart_total + footer

with open ('/home/rajarshi/Documents/Projects/COVIDTRACKER/trendAnalysis.htm', 'w') as fp: 
    fp.write(data)
    
date_time_exe = now.strftime("%H:%M:%S")

ftp = ftplib.FTP('ftpupload.net')
ftp.login('epiz_25611672','u1bLP9TbFm')
ftp.cwd('htdocs')

file1 = open('/home/rajarshi/Documents/Projects/COVIDTRACKER/index.htm','rb')
file2 = open('/home/rajarshi/Documents/Projects/COVIDTRACKER/trendAnalysis.htm','rb')

ftp.storlines('STOR index.htm', file1)
ftp.storlines('STOR trendAnalysis.htm', file2)

file1.close()
file2.close()

date_time_upload = now.strftime("%H:%M:%S")

print("Operation Executed at {} and Files Uploaded ot {}".format(date_time_exe, date_time_upload))
