import lxml
from bs4 import BeautifulSoup
import urllib.request, urllib.error
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# 明日の日付
TODAY = datetime.today()
TOMORROW = TODAY +timedelta(days=1)

driver = webdriver.Chrome()

# 明日の開催場リストのページ
print('Get Date:',datetime.strftime(TOMORROW, '%Y/%m/%d'))
URL_TOMORROW = 'https://nar.netkeiba.com/top/?kaisai_date=' + datetime.strftime(TOMORROW, '%Y%m%d') + '&rf=race_list'
driver.get(URL_TOMORROW)
WebDriverWait(driver, 10)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

#開催場所を取得します
print("koko")
RACE_LOCATIONS = soup.select(".RaceList_Body .RaceList_Top")
print("RACE_LOCATIONS" , RACE_LOCATIONS)
RACE_LOCATION = [ i.select("a") for i in RACE_LOCATIONS ]
for URL_ in  RACE_LOCATION:
    print(URL_)
print("RACE_LOCAT", RACE_LOCATION)
'''
for URL_LOCATIONS in RACE_LOCATIONS:
    print("ru")
    CURRENT_URL_LOCATION = driver.current_url
    URL_LOCATION = URL_LOCATIONS.find("a")
    print(URL_LOCATION)
    URL_LOCATION.click()
    time.sleep(3)


    # 該当競馬場のすべてのレースを取得します
    RACE_LISTS = driver.find_elements(By.CLASS_NAME, "RaceList_PrivinceSelect")
    URL_RACE_LISTS = [j for j in RACE_LISTS]
    for URL_RACE_LIST in URL_RACE_LISTS:
        CURRENT_URL_RACE_LIST = driver.current_url
        print('Race Location: ', URL_RACE_LIST)
        URL_RACE_LIST.click()
        time.sleep(3)

'''

'''
        # 該当レースのすべての馬を取得します
        HORSE_NAME = driver.find_elements(By.CSS_SELECTOR, ".HorseName")
        i = 0
        for r in HORSE_NAME:
            print(i, str(r.text))
            i += 1
            time.sleep(1)
        '''
#driver.get(CURRENT_URL_RACE_LIST)
#driver.get(CURRENT_URL_LOCATION)

driver.quit()