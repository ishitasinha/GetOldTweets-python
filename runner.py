from subprocess import call
import subprocess
import time
from datetime import datetime, timedelta
import json
import requests
import numpy as np
import matplotlib.pyplot as plt

startDateStr = '2017-11-02'
StartDateStr = '2017-11-02'
startDate = datetime.strptime(startDateStr,'%Y-%m-%d')

endDateStr = '2017-11-07'
endDate = datetime.strptime(endDateStr,'%Y-%m-%d')

dateDiff = (endDate - startDate).days
print(dateDiff)

fileName = 'Exporter.py'
querySearch = 'KSRTC'
#runFile = fileName + ' --querysearch ' + querySearch + ' --since ' + startDate + ' --until ' + endDate
#code=<get code from kshitij>
Code = 'ACC'
#UnitTime=<get time unit from kshitij>
UnitTime = 1

while endDate > startDate:
	limitDate = startDate
	limitDate += timedelta(days = 1)
	limitDateStr = limitDate.strftime('%Y-%m-%d')

	subprocess.call(['python', 'Exporter.py', '--querysearch', querySearch, '--since', startDateStr, '--until', limitDateStr])

	startDate += timedelta(days = 1)

response = requests.get('https://www.quandl.com/api/v3/datasets/NSE/'+Code+'.json?api_key=iRtWecmWy_bvJZuP-zu_')
data = response.json()

if UnitTime == 1 :
    i = 0
    a = []
    b = []
    l = len(data["dataset"]["data"]) 
    while i < l-1 :
	if data["dataset"]["data"][i][0] == startDateStr :
		break

	i = i + 1
    while i > 0  and data["dataset"]["data"][i][0] != endDateStr :
		
		y_temp1 = data["dataset"]["data"][i][5]
		y_temp2 = data["dataset"]["data"][i][5] - data["dataset"]["data"][i][1]
		x_temp = data["dataset"]["data"][i][0]
		a = np.append(a, [x_temp, y_temp1])
		b = np.append(a, [x_temp, y_temp2])
		i = i - 1
print(b)
with open('storeData.json') as f:
    floatContent = f.readlines()

floatContent = [x.strip() for x in floatContent]
bLen = len(b)
j = 1
stocks = []
while j<=bLen :
	stocks = np.append(stocks, b[j])
	j += 2

print(floatContent)

x = np.array(floatContent)
y = x.astype(np.float)
print("Sentiment change")
print(y)
z = stocks.astype(np.float)
print("Stock value change change")
print(z)

plt.plot(z, y, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)

plt.ylim(1,30)
plt.xlim(1,30)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

plt.title('Some cool customizations!')
 
# function to show the plot
plt.show()





    #post a b




'''sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

data = np.load('clusterable_data.npy')

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.title('Clusters found by {}'.format(str(algorithm._name_)), fontsize=24)
    plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)


Labels = plot_clusters(data, cluster.KMeans, (), {'n_clusters':6}).labels
'''


