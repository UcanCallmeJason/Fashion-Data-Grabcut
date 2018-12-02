# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 19:44:50 2018
인스타그램 크롤링
"""
'''
import sys
sys.path.append("D:\python3.6\Lib\site-packages\selenium\webdriver\chrome")
'''
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup


'''
# 웹페이지에 request를 보내 결과 html을 받는다.
def get_html(url): 
    _html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
        
    return _html
'''
url = "https://www.instagram.com/apckr/?hl=ko"

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe', chrome_options=options)
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')
tag = soup.find("span",
                 {"class": "qzihg"})
textonly = tag.text
print(textonly)
    
