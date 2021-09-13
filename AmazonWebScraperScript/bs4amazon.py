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

driver = webdriver.Chrome()
        
def get_url(search_term):
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    url += '&page{}' 
    return url

def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    href = 'https://amazon.in' + atag.get('href')
    
    try:
        price = item.find('span', 'a-price')
        price_parent = price.find('span', 'a-offscreen').text
    except AttributeError:
        return
    try:
        rating = item.i.text
        re_count = item.find('span', {'class':'a-size-base'}).text
    except AttributeError:
        rating = ''
        re_count = ''
    
    result = (description, price_parent, rating, re_count, href)
    return result

def main(search_term):
    driver = webdriver.Chrome()
    records = []
    url = get_url(search_term)
    
    for page in range(1,21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})
        
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()
    
    with open('results.csv', 'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price','Rating', 'RewviewCount', 'url'])
        writer.writerows(records)
        
        
main('Toys')























