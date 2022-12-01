import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas
import os

##### for character corruption
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc')

##### get x,y from csv
def plot_x(csv_file):
    csv_x = pandas.read_csv(csv_file, sep=',', encoding='utf-8', parse_dates=True, usecols=[0]).values
    x = []
    for i in csv_x:
        for j in i:
            j = pandas.to_datetime(j)
            x.append(j)
    return x

def plot_y(csv_file):
    csv_y = pandas.read_csv(csv_file, sep=',', encoding='utf-8', parse_dates=True, usecols=[1]).values
    y = []
    for i in csv_y:
        for j in i:
            j = pandas.to_datetime(j)
            y.append(j)
    return y



##### input race day
def input_race_day():
    while True:
        race_day = input("[Default:tomorrow, 1key:today, 8key:input date]")
        if len(str(race_day)) == 1:
            today = datetime.today()
            str_today = datetime.strftime(today, '%Y%m%d')
            return str_today
        elif len(str(race_day)) == 0:
            tomorrow = datetime.today()+timedelta(days=1)
            str_tomorrow = datetime.strftime(tomorrow, '%Y%m%d')
            return str_tomorrow
        elif len(str(race_day)) == 8:
            return race_day
        else:
            print("wrong input")
            break

race_day = str(input_race_day())

##### check file path
dir_listBox = 'log/'+str(race_day)+'/'
if os.path.isdir(dir_listBox):
    for track in os.listdir(dir_listBox):
        print(track)
        
        for num in os.listdir(dir_listBox+track):
            print(num)
            if not num.endswith('.png'):


                ##### create plot
                ax = plt.subplot()
                plt.title(track + num, fontproperties=fp)
                plt.xlabel("date")
                plt.ylabel("time")

                labels = ax.get_xticklabels()
                plt.setp(labels, rotation=45)
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
                ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                plt.grid()

                for order in os.listdir(dir_listBox+track+'/'+num):
                    print(order)
                    if order.endswith('.csv'):
                        csv_file = dir_listBox+'/'+track+'/'+num+'/'+order
                        ax.plot(plot_x(csv_file), plot_y(csv_file), label=order[:-4])
                        plt.legend(prop={'family':'MS Gothic'})

                # create new file.
                save_dir = 'log/'+str(race_day)+'/'+str(track)+'/'+num+'.png'
                plt.savefig(save_dir)
                plt.close()

# x軸の間隔を固定する