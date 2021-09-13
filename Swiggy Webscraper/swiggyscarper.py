# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 16:26:31 2021

@author: PAARTH
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd

def get_url(city_name,number_of_pages):
    url = f"https://www.swiggy.com/{city_name}?page={number_of_pages}"
    return url

def extract(city,pages):
    restaurant = []
    restaurant_type2 = []
    restaurant_rating = []
    restaurant_2 = []
    for i in range(1,15):
        driver = webdriver.Chrome()
        driver.get(get_url(city,i))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'class':'_1HEuF'})
        for result in results:
            names = soup.find_all('div',{'class':'nA6kb'})
            restaurant_type = soup.find_all('div',{'class':'_1gURR'})
            ratings = soup.find_all('div', {'class':'_9uwBC wY0my'})
            price_for_two = soup.find_all('div',{'class':'nVWSi'})
        for name in names:
            restaurant.append(name.text)
        for types in restaurant_type:
            text1 = types.get_text()
            restaurant_type2.append(text1)
        for rating in ratings:
            restaurant_rating.append(rating.text)
        for prices in price_for_two:
            restaurant_2.append(prices.text)
        driver.close()
                
    return restaurant, restaurant_type2, restaurant_rating, restaurant_2
        

restaurant, restaurant_type2, restaurant_rating, restaurant_2 = extract('delhi',20)
final = [restaurant, restaurant_type2, restaurant_rating, restaurant_2]
with open('results.csv', 'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price','Rating', 'RewviewCount', 'url'])
        writer.writerows(final)

dict_1 = {'Restaurant_Name':restaurant, 'Restaurant_Category':restaurant_type2,
          'Restaurant_Rating':restaurant_rating, 'Price_For_Two':restaurant_2}

df1 = pd.DataFrame(restaurant, columns=['Restaurant_Name'])
df2 = pd.DataFrame(restaurant_type2, columns=['Restaurant_Category'])
df3 = pd.DataFrame(restaurant_rating, columns=['Rating'])
df4 = pd.DataFrame(restaurant_2, columns=['price_for_2'])

df_final = pd.DataFrame(df1['Restaurant_Name'], columns=df1.columns)
df_final['Restaurant_Category'] = df2['Restaurant_Category']
df_final['Rating'] = df3['Rating']
df_final['price_for_2'] = df4['price_for_2']

pd.DataFrame.to_csv(df_final, 'results.csv')
















































































# to do
# cutsom url
# extraction functions








































































































































