import lxml
import time
import csv
import os
import pandas
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

# select race_date
TARGET_day = input('[Default:tomorrow, 1key:today]')
today = datetime.today()
tomorrow = today +timedelta(days=1)
if len(TARGET_day) == 0:
    race_day = datetime.strftime(tomorrow, '%Y%m%d')
elif len(TARGET_day) == 1:
    race_day = datetime.strftime(today, '%Y%m%d')
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
    progressTrack = ' track:' + str(name_track) + '/' + str(len_LIST_track)
    progressList = '    Progress:' + progressHorse + progressNum + progressTrack
    print('[Creating]', path, progressList)

'''# for view complete time
current_time = datetime.now()
def progress(race_day, current_time):
    days = race_day-alpha_day
    complete_hours = (datetime.now()-current_time).seconds*days.days/3600
    print('remaining download time '+str(complete_hours)+'hours ')
    return datetime.now()'''

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
    #if not name_track == '園田':
    #    continue

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
        #if int(num[:-1]) < 12:
        #    continue

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

            # get horse order
            order = LIST_horse.index(horse) + 1


            ##### get list of results
            url_table = url_horse+'/html/body/div[1]/div[2]/div[class="db_main_race"]/div[calss="db_main_data"]/table[class="db_h_race_results"]'
            LISTs = pandas.read_html(url_table,encoding='euc-jp')[3]
            if len(LISTs.columns) < 3:
                i = 3
                while True:
                    LISTs = pandas.read_html(url_table,encoding='euc-jp')[i]
                    if len(LISTs.columns) < 3:
                        break
                    i += 1
            LISTs = LISTs.loc[:,['日付','開催','天 気','R','頭 数','馬 番','オ ッ ズ','人 気','着 順','騎手','斤 量','距離','馬 場','タイム','着差','通過','ペース','上り','馬体重','賞金']]
            LISTs.dropna(inplace=True)
            LISTs = LISTs[LISTs['開催']==name_track]
            LISTs = LISTs[LISTs['距離']==TARGET_distance]

            ##### log progress 
            logForProgress(race_day, name_track, num, len_LIST_track, len_LIST_num, len_LIST_horse)


            ##### create new directory
            file_dir = 'log/'+str(race_day)+'/'+str(name_track)+'/'+str(num)+'/'
            csv_file = file_dir + str(order)+'_'+str(horse)

            if os.path.isdir(file_dir) == False:
                os.makedirs(file_dir)
            
            # add results to file.csv
            LISTs.to_csv(csv_file+'.csv',mode='w',encoding='shift-jis',index=None)