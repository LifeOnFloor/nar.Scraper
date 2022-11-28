import lxml
import time
import csv
import os
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


####################
####
####    requests
####
####################

# 馬番を併記したい

####################
####
####    var List
####
####################

# url='地方競馬のトップページ'
#
# tomorrow='明日の日付'
# URL_tomorrow='明日のURL'
#
# name_track='開催日の開催場'
# url_track='開催日の開催場ごとのURL'
#
# num='開催場のレース番号'
# url_num='開催場のレースURL'
#
# TARGET_distance='今走のレース条件（ダ1400など）'
# horse='今走の馬名'
# URL_horse='今走の馬ページURL '
#
# track='result track'
# distance='result distance'
# condition='result condition'
# date='result date'
# result='result time'
#



####################
####
####    Setting
####
####################

url = 'https://nar.netkeiba.com/'

# select race condition [Default:良,2:稍,3:重,4:不]
TARGET_condition = input('input 2 or 3 or 4 or Enter as 1: ')
if TARGET_condition == 2:
    TARGET_condition = '稍'
elif TARGET_condition == 3:
    TARGET_condition = '重'
elif TARGET_condition == 4:
    TARGET_condition = '不'
else:
    TARGET_condition = '良'

# select race_date
TARGET_day = input('input yyyymmdd or Enter as tomorrow: ')
today = datetime.today()
tomorrow = today +timedelta(days=1)
if len(TARGET_day) == 0:
    race_day = datetime.strftime(tomorrow, '%Y%m%d')
else:
    race_day = TARGET_day
print('Get race day : ' + race_day)



####################
####
####    Function
####
####################

def waitForLoad(driver):
    i = 0
    elem = driver.find_elements(By.TAG_NAME, "html")
    while True:
        if len(elem) > 0:
            time.sleep(1)
            return
        if i == 20:
            print('waited 10s')
            return
        else:
            i += 1
            time.sleep(.5)



####################
###
###    driver setting
###
####################

# option
options = Options()
options.add_argument("--headless")
options.add_argument("log-level=3")
options.add_argument("disable-logging")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# get driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), service_log_path = "NUL", options = options)



####################
###
###    main
###
####################

##### jump to/target/date

driver.get(url + '?kaisai_date=' + race_day + '&rf=race_list')
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

waitForLoad(driver)



##### select the track

TRACKs = soup.select("ul.RaceList_ProvinceSelect > li > a")

URLs_track = [i.get("href") for i in TRACKs]
NAMEs_track = [i.getText() for i  in TRACKs]

for (name_track, url_track) in zip(NAMEs_track, URLs_track):

    driver.get(url + url_track)
    waitForLoad(driver)

    html_track = driver.page_source
    soup_track = BeautifulSoup(html_track, 'lxml')



    ##### select the race

    RACEs = soup_track.select("li.RaceList_DataItem > a")
    LISTs_num = soup_track.select("li.RaceList_DataItem > a > div.Race_Num > span")

    LIST_num = [i.getText() for i in LISTs_num]
    LIST_urls_num = [i.get("href") for i in RACEs]
    urls_num = [i for i in LIST_urls_num  if i[:12] != '../race/movie']

    for num,url_num in zip(LIST_num, urls_num):
        if url_num[:15] == '../race/shutuba':
            url_num = url_num[2:]
            
        driver.get(url + url_num)
        waitForLoad(driver)

        html_horse = driver.page_source
        soup_horse = BeautifulSoup(html_horse, 'lxml')



        ##### get the race info

        TARGET_distance = soup_horse.select_one("div.RaceData01 > span").getText()[1:-1]


            
        ##### create new file.csv
        if os.path.isdir('log/'+race_day+'/'+name_track) == False:
            os.makedirs('log/'+race_day+'/'+name_track)

        with open('log/'+race_day+'/'+name_track+'/'+race_day+'_'+name_track+'_'+num+'.csv', 'w', newline='', encoding='UTF-8') as f:
            write = csv.writer(f)
            write.writerow(['track + num', 'distance', 'condition', 'horse', 'result_day', 'result_time'])



        ##### select the horse

        LISTs_horse = soup_horse.select("span.HorseName > a")
        LIST_horse = [i.getText() for i in LISTs_horse]
        urls_horse = [i.get("href") for i in LISTs_horse]



        ##### get the horse

        for horse, url_horse in zip(LIST_horse, urls_horse):
            driver.get(url_horse)
            waitForLoad(driver)
            html_result = driver.page_source
            soup_horse = BeautifulSoup(html_result, 'lxml')



            ##### get the results

            LISTs = soup_horse.select('table.db_h_race_results > tbody > tr > td')
            
            LISTs_track = LISTs[1::28]
            LISTs_race_day = LISTs[0::28]
            LISTs_distance = LISTs[14::28]
            LISTs_condition = LISTs[15::28]
            LISTs_time = LISTs[17::28]

            LIST_track = [i.getText() for i in LISTs_track]
            LIST_race_day = [i.getText() for i in LISTs_race_day]
            LIST_condition = [i.getText() for i in LISTs_condition]
            LIST_distance = [i.getText() for i in LISTs_distance]
            LIST_time = [i.getText() for i in LISTs_time]



            ##### output results to file.csv

            print(name_track, num, horse)

            for track, distance, condition, result_day, result in zip(LIST_track, LIST_distance, LIST_condition, LIST_race_day, LIST_time):

                if track == name_track and distance == TARGET_distance and condition == TARGET_condition and len(result) != 0:
                    print(name_track + num, distance, condition, horse, result_day, result)
                    with open('log/'+race_day+'/'+track+'/'+race_day+'_'+name_track+'_'+num+'.csv', 'a', newline='', encoding='UTF-8') as f:
                        write = csv.writer(f)
                        write.writerow([name_track + num, distance, condition, horse, result_day, result])