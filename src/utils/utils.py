import requests
import base64
import re

import utils.env as env
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By



def getAnimeList():


    """Start web driver"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    url = 'https://anichart.net/Winter-2022'
    url = 'https://anilist.co/search/anime?year=2022&season=WINTER&format=TV'
    url = 'https://anilist.co/search/anime/this-season'


    driver.get(url)

    print(f"Store airing: [{driver.title}] ", flush=True)

    match = re.search(r'^(\w+)\s(\w+)\s(\w+)\s', driver.title)
    if match:
        print(match.group())   
        print(match.group(1))  
        print(match.group(2))  
    
        url = f'https://anilist.co/search/anime?year={match.group(2)}&season={match.group(1).upper()}&format=TV'
        
        print(f" ==> url: [{url}] ", flush=True)
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)
        browser.implicitly_wait(10)


    return browser



def scrollDown(driver, value):
    driver.execute_script("window.scrollBy(0,"+str(value)+")")



