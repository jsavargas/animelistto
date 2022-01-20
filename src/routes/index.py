import json
import requests
import base64
import os
import sys
import shutil
import time
import json
import datetime  



from tqdm import tqdm
from bs4 import BeautifulSoup

import utils.env as env

import utils.utils 



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
def home():
    page = request.args.get('page', default = 1, type = int)
    perPage = request.args.get('perPage', default = 50, type = int)
    season = request.args.get('perPage', default = 'season: WINTER', type = str)



    response = utils.utils.getSeasonAnimeList()



    datas = json.loads(response.text)
    media = []

    for data in datas['data']['Page']['media']:
        print(f'page_source => while True  => {json.dumps(data, indent=4)} ', flush=True)
        try:
            media.append( {
                "idMal": f"https://myanimelist.net/anime/{data['idMal']}/",
                "name": data['title']['english'] if data['title']['english'] is not None else data['title']['romaji'],
                "romaji": data['title']['romaji'],
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
                "startDate":data['startDate'],
                "endDate":data['endDate'],
            } )
        except:
            continue

    media_sorted = sorted(
        media, key=lambda x:( x["airing"] is None ,x["airing"] == '' , x["airing"],  x["status"]), reverse=False
    )


    #data = list(dict.fromkeys(data))

    return render_template(
        "index.html",  data=media_sorted
    )
    return response.text


@index.route("/anime")
def anime():
    page = request.args.get('page', default = 1, type = int)
    perPage = request.args.get('perPage', default = 50, type = int)
    year = request.args.get('year', default = datetime.datetime.now().year, type = int)


    response = utils.utils.getYearAnimeList(page=page,year=year)



    datas = json.loads(response.text)
    media = []

    for data in datas['data']['Page']['media']:
        print(f'page_source => while True  => {json.dumps(data, indent=4)} ', flush=True)
        try:
            media.append( {
                "idMal": f"https://myanimelist.net/anime/{data['idMal']}/",
                "name": data['title']['english'] if data['title']['english'] is not None else data['title']['romaji'],
                "romaji": data['title']['romaji'],
                "img_src": data['coverImage']['extraLarge'],
                "airing" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] ) if data['nextAiringEpisode'] is not None else '' ,
                "airing_mod" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] ).strftime( "%Y-%m-%d") if data['nextAiringEpisode'] is not None else '' ,
                "format":data['format'],
                "description":data['description'],
                "hashtag":data['hashtag'],
                "season":data['season'],
                "next_episode":data['nextAiringEpisode']['episode'] if data['nextAiringEpisode'] is not None else '',
                "status":data['status'],
                "episodes":data['episodes'],
                "startDate":data['startDate'],
                "endDate":data['endDate'],
            } )
        except:
            continue

 
    media_sorted = sorted(
        media, key=lambda x:( x["airing"] is None ,x["airing"] == '' , x["airing"],  x["status"]), reverse=False
    )

    return render_template(
        "index.html",  data=media_sorted
    )
    return response.text





