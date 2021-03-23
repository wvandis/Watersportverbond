# -*- coding: utf-8 -*-
from selenium import webdriver #3.141.0
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
import os
import pandas as pd
import numpy as np
import re
import time

# settings 
url_wedstrijdzeilen='https://www.watersportverbond.nl/kalender/wedstrijden/zeilen'
path = os.path.dirname(os.path.abspath(__file__))

# Chrome will be used
options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--incognito')
# setting up selenium driver
driver = webdriver.Chrome(options=options, executable_path=os.path.join(path,'chromedriver'))

# opening the website	
driver.get(url_wedstrijdzeilen)

def by_class(class_name, column_name):
    content = driver.find_elements_by_class_name(class_name)
    text = [x.text for x in content]
    df = pd.DataFrame(text, columns=[column_name])
    
    return df

df_complete=[]
x=1
while x==1:
    # catching event name and club
    df = by_class('item','Content')
    df=df['Content'].str.split('\n',n=2, expand=True)
    df.columns=['Datum','Event','Club']
    # regex to remove tekst string
    df['Club'].replace(r'Aan je agenda.*[\n].*|[\n]Aan .*[\n].*','',regex=True, inplace=True)
    df['Club'].replace(r'[\n]',', ',regex=True, inplace=True)

    if len(df_complete)==0:
        df_complete=df
    else:
        df_complete=df_complete.append(df)

    # print out all the titles.
    print(df_complete)

    try:
        # getting the next button by class name
        button=driver.find_element_by_xpath("""/html/body[@class='template-calendaritemoverviewpage']/div[@id='scrollto-content']/div[@id='initiative-search']/div[@class='g-size-12 g-size-lg-8 faceted-search__results']/div[@class='pagination__container']/ul[@class='pagination']/li[@class='pagination__item pagination__item--next']/a""")
        # clicking the button
        driver.execute_script("arguments[0].click();", button)
    except:
        x=0

    time.sleep(5)

df_complete.to_excel('watersportverbond.xlsx',sheet_name='zeilen')

# closing connection
driver.close()

