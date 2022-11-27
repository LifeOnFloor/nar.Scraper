import lxml
import time
from bs4 import BeautifulSoup
import urllib.request, urllib.error
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

##############
#
#　設定
#
##############

# [良,稍,重,不]を選択
TARGET_CONDITION = '良'


##############
#
#　本体
#
##############

URL = 'https://nar.netkeiba.com/'
driver = webdriver.Chrome()



# 明日の開催場所トップページへ遷移する
TODAY = datetime.today()
TOMORROW = TODAY +timedelta(days=1)

URL_TOMORROW = URL + '?kaisai_date=' + datetime.strftime(TOMORROW, '%Y%m%d') + '&rf=race_list'

print('Get Date:',datetime.strftime(TOMORROW, '%Y/%m/%d'))

driver.get(URL_TOMORROW)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

WebDriverWait(driver, 10)



# 開催されている競馬場をひとつずつ選択する

TRACKS = soup.select("ul.RaceList_ProvinceSelect > li > a")

URL_TRACK = [ i.get("href") for i in TRACKS ]
NAME_TRACK = [ i.getText() for i  in TRACKS ]

for (name,url_loc) in zip(NAME_TRACK, URL_TRACK):
    driver.get(URL + url_loc)
    WebDriverWait(driver, 10)
    time.sleep(3)



    # レースをひとつずつ選択する

    RACE = soup.select("li.RaceList_DataItem > a")
    RACE_NUMS = soup.select("li.RaceList_DataItem > a > div.Race_Num > span")

    RACE_NUM = [ i.getText() for i in RACE_NUMS ]
    URL_NUM = [ i.get("href") for i in RACE ]

    for num,url_num in zip(RACE_NUM, URL_NUM):
        url_num = url_num[3:]
        print(name , num, URL + url_num)
        driver.get(URL + url_num)
        WebDriverWait(driver, 10)
        time.sleep(3)



        # レース条件を取得する

        html_horse = driver.page_source
        soup_horse = BeautifulSoup(html_horse, 'lxml')
        TARGET_DISTANCE = soup_horse.select_one("div.RaceData01 > span").getText()[1:-1]
        TARGET_TRACK = soup_horse.select("div.RaceData02 > span")[1].getText()
        print(TARGET_TRACK)



        # 馬を1頭ずつ選択する

        HORSES_LIST = soup_horse.select("span.HorseName > a")
        HORSES = [ i.getText() for i in HORSES_LIST ]
        URL_HORSES = [ i.get("href") for i in HORSES_LIST ]

        for HORSE, URL_HORSE in zip(HORSES, URL_HORSES):
            driver.get(URL_HORSE)

            WebDriverWait(driver, 10)
            time.sleep(3)
            


            # 戦績を取得する

            html_result = driver.page_source
            soup_horse = BeautifulSoup(html_result, 'lxml')

            RESULTS_LIST = soup_horse.select('table.db_h_race_results > tbody > tr > td')
            
            RESULTS_LIST_TRACK = RESULTS_LIST[1::28]
            RESULTS_LIST_DATE = RESULTS_LIST[0::28]
            RESULTS_LIST_DISTANCE = RESULTS_LIST[14::28]
            RESULTS_LISTS_CONDITION = RESULTS_LIST[15::28]
            RESULTS_LIST_TIME = RESULTS_LIST[17::28]

            RESULTS_TRACK = [i.getText() for i in RESULTS_LIST_TRACK]
            RESULTS_DATE = [i.getText() for i in RESULTS_LIST_DATE]
            RESULTS_CONDITION = [i.getText() for i in RESULTS_LISTS_CONDITION]
            RESULTS_DISTANCE = [i.getText() for i in RESULTS_LIST_DISTANCE]
            RESULTS_TIME = [i.getText() for i in RESULTS_LIST_TIME]



            # 該当競馬場、該当距離、該当馬場状態（デフォルト：良）の走破タイムを出力

            for RESULT_TRACK, RESULT_DATE, RESULT_CONDITION, RESULT_DISTANCE, RESULT_TIME in zip(RESULTS_TRACK, RESULTS_DATE, RESULTS_CONDITION, RESULTS_DISTANCE, RESULTS_TIME):
                if RESULT_TRACK == TARGET_TRACK and RESULT_DISTANCE == TARGET_DISTANCE and RESULT_CONDITION == TARGET_CONDITION:
                    print(RACE_NUM, RESULT_TRACK, HORSE, RESULT_DISTANCE, RESULT_CONDITION, RESULT_DATE, RESULT_TIME)

            WebDriverWait(driver, 10)
            time.sleep(1)