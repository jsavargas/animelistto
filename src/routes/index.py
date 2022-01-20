import json
import requests
import base64
import os
import sys
import shutil
import time
import json
import datetime  

import datetime as dt
import xml.etree.ElementTree as ET

from tqdm import tqdm
from bs4 import BeautifulSoup

import utils.env as env

from utils.utils import getAnimeList, scrollDown

from selenium.webdriver.support.ui import WebDriverWait


from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
)


index = Blueprint("index", __name__)

connection = []
linksDownloads = []


@index.route("/")
def homea():

    query = '''
        query ($page: Int, $perPage: Int) {
            Page(page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
                media(type: ANIME, sort: TRENDING_DESC) {
                id
                title {
                    romaji
                    english
                    native
                    userPreferred
                }
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                coverImage {
                    extraLarge
                    large
                    medium
                }
                bannerImage
                format
                type
                status
                episodes
                chapters
                volumes
                season
                description
                averageScore
                meanScore
                genres
                synonyms
                hashtag
                source
                isAdult
                isFavourite
                nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
                }
                siteUrl
                
            }
        }
        }
    '''
    variables = {
        'page': 1,
        'perPage': 55
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})



    datas = json.loads(response.text)
    media = []

    for data in datas['data']['Page']['media']:
        print(f'page_source => while True  => {json.dumps(data, indent=4)} ', flush=True)
        try:
            media.append( {
                "name": data['title']['english'],
                "img_src": data['coverImage']['extraLarge'],
                "airing" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] )  ,
                "airing_mod" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] ).strftime( "%Y-%m-%d")  ,
                "format":data['format'],
                "description":data['description'],
                "hashtag":data['hashtag'],
                "season":data['season'],
                "next_episode":data['nextAiringEpisode']['episode'],
                "status":data['status'],
                "episodes":data['episodes'],
            } )
        except:
            continue

    media_sorted = sorted(
        media, key=lambda x: x["airing"], reverse=False
    )


    #data = list(dict.fromkeys(data))

    return render_template(
        "index.html",  data=media_sorted
    )
    return response.text




@index.route("/home")
def home():





    driver = getAnimeList()

    old_page = driver.page_source
    

    while True:
        for i in range(2):
            scrollDown(driver, 500)
            time.sleep(2)
        new_page = driver.page_source
        print(f'page_source => while True  => ', flush=True)
        if new_page != old_page:
            old_page = new_page
        else:
            break






    html_after_JS = driver.execute_script("return document.body.innerHTML")


    #contents = driver.find_elements_by_class_name('media-card')
    #soup = BeautifulSoup(driver.page_source, 'html.parser')
    #token = soup.find("a", {"class": "title"})
    
    
    
    #print(f'page_source => Successfully accessed  => {html_after_JS}', flush=True)
    print(f'*'*50, flush=True)
    print(f'*'*50, flush=True)
    print(f'*'*50, flush=True)
    print(f'*'*50, flush=True)
    print(f'*'*50, flush=True)
    print(f'*'*50, flush=True)
    #print(f'contents => Successfully accessed  => {contents}', flush=True)
    #print(f'contents => Successfully accessed  => {len(contents)}', flush=True)


    data = []


    soup = BeautifulSoup(old_page, 'html.parser')
    media_card = soup.find_all("div", {"class": "media-card"})

    alias = soup.find('h1', {'class': 'alias-title'})
    
    
    
    #print(f"Store html_after_JS: {html_after_JS} ", flush=True)





    for media in media_card:
        title = media.find("a", {"class": "title"})
        img_src = media.find("img", {"class": ["image", "loaded"]})
        airing = media.find("div", {"class":["airing"]})
    
        print(f'*'*50, flush=True)

        print(f"Store title: [{title.text}] ", flush=True)
        print(f"Store airing: [{airing}] ", flush=True)
        print(f"Store airing: [{driver.title}] ", flush=True)



        

        data.append( {
            "name": title.text,
            "img_src": img_src['src'],
            "airing":airing
        } )

    #data = list(dict.fromkeys(data))


    return render_template(
        "index.html", token=driver.title, data=data
    )



