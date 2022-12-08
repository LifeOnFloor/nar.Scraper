import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas
import os


# for character corruption
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\msgothic.ttc')

# for select track condition
_condition = ['良','稍','重','不']


##########
#
#   function
#
##########

# save plot to file.png
def plot(csv_file, dir_track, dir_file):
    input_file = dir_file+'/'+csv_file

    # plot by track condition
    for i in range(4):
        if i == 0:
            ax0.set_title(track + num + _condition[i], fontproperties=fp)
            ax0.plot(plot_x(input_file,i), plot_y(input_file,i), label=csv_file[:-4])
            ax0.legend()
            ax0.legend(prop={'family':'MS Gothic'})
            labels = ax0.get_xticklabels()
            ax0.set_label(labels)

        if i == 1:
            ax1.set_title(track + num + _condition[i], fontproperties=fp)
            ax1.plot(plot_x(input_file,i), plot_y(input_file,i), label=csv_file[:-4])
            ax1.legend()
            ax1.legend(prop={'family':'MS Gothic'})
            labels = ax1.get_xticklabels()
            ax1.set_label(labels)

        if i == 2:
            ax2.set_title(track + num + _condition[i], fontproperties=fp)
            ax2.plot(plot_x(input_file,i), plot_y(input_file,i), label=csv_file[:-4])
            ax2.legend()
            ax2.legend(prop={'family':'MS Gothic'})
            labels = ax2.get_xticklabels()
            ax2.set_label(labels)

        if i == 3:
            ax3.set_title(track + num + _condition[i], fontproperties=fp)
            ax3.plot(plot_x(input_file,i), plot_y(input_file,i), label=csv_file[:-4])
            ax3.legend()
            ax3.legend(prop={'family':'MS Gothic'})
            labels = ax3.get_xticklabels()
            ax3.set_label(labels)
            

        print('[Create]',track, num, csv_file[:-4])
        fig.savefig(dir_track+'/'+num+csv_file[-4]+'.png')


# track condition
def condition(csv_file,baba):
    df = pandas.read_csv(csv_file, sep=',',usecols=['馬 場','日付','タイム'], encoding='shift-jis', parse_dates=True)
    df = df[df['馬 場'] == _condition[baba]]
    df.dropna(inplace=True)
    return df


# get x from csv
def plot_x(csv_file,baba):
    date = condition(csv_file,baba)['日付'].values.tolist()
    x = [datetime.strptime(i,'%Y/%m/%d') for i in date]
    return x

# get y from csv
def plot_y(csv_file,baba):
    time = condition(csv_file,baba)['タイム'].values.tolist()
    y = [datetime.strptime(i,'%H:%M.%S') for i in time]
    return y


# input race day
def input_race_day():
    while True:
        race_day = input("[Default:tomorrow, 1key:today]")
        if len(str(race_day)) == 1:
            today = datetime.today()
            str_today = datetime.strftime(today, '%Y%m%d')
            return str_today
        elif len(str(race_day)) == 0:
            tomorrow = datetime.today()+timedelta(days=1)
            str_tomorrow = datetime.strftime(tomorrow, '%Y%m%d')
            return str_tomorrow
        else:
            print("wrong input")
            break


race_day = str(input_race_day())


##########
#
#   main
#
##########

# check file path
dir_listBox = 'log/'+str(race_day)
if os.path.isdir(dir_listBox):
    for track in os.listdir(dir_listBox):
        #if track != '大井':
        #    continue
        dir_track = dir_listBox+'/'+track
        for num in os.listdir(dir_track):
            #if int(num[:2]) < 12:
            #    continue

            if not num.endswith('.png'):
                dir_file = dir_track+'/'+num
                
                # set before plot()
                fig = plt.figure(figsize=(15,10))
                ax0 = fig.add_subplot(2,2,1)
                ax1 = fig.add_subplot(2,2,2)
                ax2 = fig.add_subplot(2,2,3)
                ax3 = fig.add_subplot(2,2,4)

                ax0.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
                ax0.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax0.set_xlim(datetime.today()+timedelta(days=-300), datetime.today())
                ax0.set_xlabel("date")
                ax0.set_ylabel("time")
                ax0.grid()

                ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
                ax1.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax1.set_xlim(datetime.today()+timedelta(days=-300), datetime.today())
                ax1.set_xlabel("date")
                ax1.set_ylabel("time")
                ax1.grid()

                ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
                ax2.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax2.set_xlim(datetime.today()+timedelta(days=-300), datetime.today())
                ax2.set_xlabel("date")
                ax2.set_ylabel("time")
                ax2.grid()

                ax3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
                ax3.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                ax3.set_xlim(datetime.today()+timedelta(days=-300), datetime.today())
                ax3.set_xlabel("date")
                ax3.set_ylabel("time")
                ax3.grid()

                # create plot
                for csv_file in os.listdir(dir_file):
                    plot(csv_file, dir_track, dir_file)
        
        # figure need close() to next race figure
        plt.close()