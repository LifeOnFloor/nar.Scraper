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
####    Setting
####
####################

url = 'https://nar.netkeiba.com/'

# select race condition [Default:良,2:稍,3:重,4:不]
TARGET_condition = input('[Default:良, 2:稍, 3:重, 4:不]')
if TARGET_condition == 2:
    TARGET_condition = '稍'
elif TARGET_condition == 3:
    TARGET_condition = '重'
elif TARGET_condition == 4:
    TARGET_condition = '不'
else:
    TARGET_condition = '良'

# select race_date
TARGET_day = input('[Default:tomorrow, 1key:today, 8key:input date]')
today = datetime.today()
tomorrow = today +timedelta(days=1)
if len(TARGET_day) == 0:
    race_day = datetime.strftime(tomorrow, '%Y%m%d')
elif len(TARGET_day) == 1:
    race_day = datetime.strftime(today, '%Y%m%d')
elif len(TARGET_day) == 8:
    race_day = TARGET_day
else:
    print("wrong input")



####################
####
####    Function
####
####################

# manner for web server
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

# for view progress
def logForProgress(race_day, name_track, num, len_LIST_track, len_LIST_num, len_LIST_horse):
    path = str(race_day[4:])+'_'+str(name_track)+'_'+str(num)
    progressHorse = ' horse:' + str(LIST_horse.index(horse)+1) + '/' + str(len_LIST_horse)
    progressNum = ' num:' + str(LIST_num.index(num)+1) + '/' + str(len_LIST_num)
    if name_track in LIST_track and LIST_track.index(name_track) <= len_LIST_track:
        progressTrack = ' track:' + str(LIST_track.index(name_track)+1) + '/' + str(len_LIST_track)
    else:
        progressTrack = ' track:?/' + str(len_LIST_track)
    progressList = '    Progress:' + progressHorse + progressNum + progressTrack
    print('[Creating]', path, progressList)



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

##### jump to date page
driver.get(url + '?kaisai_date=' + race_day + '&rf=race_list')
waitForLoad(driver)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')



##### get list of tracks
TRACKs = soup.select(".RaceList_ProvinceSelect > li > a")
LISTs_track = [i.getText() for i in TRACKs]
URLs_track = [i.get("href") for i in TRACKs]
len_LIST_track = len(LISTs_track)

for (name_track, url_track) in zip(LISTs_track, URLs_track):

    # jump to track page
    driver.get(url + url_track)
    waitForLoad(driver)

    html_track = driver.page_source
    soup_track = BeautifulSoup(html_track, 'lxml')



    ##### get list of races
    RACEs = soup_track.select_one('[style*="display : block"]')
    LIST_num = [i.getText(strip=True) for i in RACEs.select('li.RaceList_DataItem > a > div.Race_Num > span')]
    LIST_urls_num = [i.get("href") for i in RACEs.select('li.RaceList_DataItem > a')]
    urls_num = [i for i in LIST_urls_num if not i.startswith('../race/movie')]

    # for view progress
    len_LIST_num = len(LIST_num)

    ##### jump to race page
    for (num,url_num) in zip(LIST_num, urls_num):
        driver.get(url + url_num[2:])
        waitForLoad(driver)
        html_horse = driver.page_source
        soup_horse = BeautifulSoup(html_horse, 'lxml')



        ##### get the race info
        TARGET_distance = soup_horse.select_one("div.RaceData01 > span").getText(strip=True)[:-1]



        ##### get list of horses
        LISTs_horse = soup_horse.select("span.HorseName > a")
        LIST_horse = [i.getText(strip=True) for i in LISTs_horse]
        urls_horse = [i.get("href") for i in LISTs_horse]
        len_LIST_horse = len(LIST_horse)


        ##### jump to horse page
        for (horse, url_horse) in zip(LIST_horse, urls_horse):
            driver.get(url_horse)
            waitForLoad(driver)
            html_result = driver.page_source
            soup_horse = BeautifulSoup(html_result, 'lxml')

            # get horse order
            order = LIST_horse.index(horse) + 1



            ##### get list of results
            LISTs = soup_horse.select('table.db_h_race_results > tbody > tr > td')
            
            LISTs_track = LISTs[1::28]
            LISTs_race_day = LISTs[0::28]
            LISTs_distance = LISTs[14::28]
            LISTs_condition = LISTs[15::28]
            LISTs_time = LISTs[17::28]

            LIST_track = [i.getText(strip=True) for i in LISTs_track]
            LIST_race_day = [i.getText(strip=True) for i in LISTs_race_day]
            LIST_condition = [i.getText(strip=True) for i in LISTs_condition]
            LIST_distance = [i.getText(strip=True) for i in LISTs_distance]
            LIST_time = [i.getText(strip=True) for i in LISTs_time]



            ##### log progress 
            logForProgress(race_day, name_track, num, len_LIST_track, len_LIST_num, len_LIST_horse)


            ##### create new directory
            file_dir = 'log/'+str(race_day)+'/'+str(name_track)+'/'+str(num)+'/'
            csv_file = file_dir + str(order)+'_'+str(horse)+'.csv'

            if os.path.isdir(file_dir) == False:
                os.makedirs(file_dir)
            
            # create new file.csv
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    write = csv.writer(f)
                    write.writerow(['date', 'time'])

            # add results to file.csv
            for (track, distance, condition, result_day, result) in zip(LIST_track, LIST_distance, LIST_condition, LIST_race_day, LIST_time):
                if track == name_track and distance == TARGET_distance and condition == TARGET_condition and len(str(result)) != 0:

                    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                        write = csv.writer(f)
                        write.writerow([result_day, result])