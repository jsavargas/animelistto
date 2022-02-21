import json
import requests
import base64
import os
import sys
import shutil
import time
import json
import datetime  
import sqlite3



from tqdm import tqdm
from bs4 import BeautifulSoup

import utils.env as env

import utils.utils 
from utils.log import logger
import utils.sonarr as sonarr
import controller.db as database



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
con = sqlite3.connect('/config/anime.db')

connection = []
linksDownloads = []


@index.route("/")
def home():
    page = request.args.get('page', default = 1, type = int)
    perPage = request.args.get('perPage', default = 50, type = int)
    season = request.args.get('perPage', default = 'season: WINTER', type = str)


    logger("home()")

    #Sonarr = (sonarr.Sonarr('http://192.168.0.10:8989', '61db77c5ec5b4bc3be57ab3a3f1e36e2')
    Sonarr = ( sonarr.Sonarr('http://192.168.0.10:8989', '61db77c5ec5b4bc3be57ab3a3f1e36e2') )

    _root_folders = Sonarr.get_root_folders()
    _all_tags = Sonarr.get_all_tags()
    _quality_profile_id = Sonarr.lookup_quality_profile_id()


    media_sorted = []
    respSonarr = [] 
    #return render_template(
    #    "index.html",  data=media_sorted,sonarr=respSonarr, root_folders = _root_folders, all_tags = _all_tags, quality_profile_id= _quality_profile_id
    #)



    response = utils.utils.getSeasonAnimeList()


    datas = json.loads(response.text)
    media = []
    respSonarr = []

    for data in datas['data']['Page']['media']:
        print(f'page_source => while True  => {json.dumps(data, indent=4)} ', flush=True)
        try:
            results = []
            #results = Sonarr.lookup_series(data['title']['english'] if data['title']['english'] is not None else data['title']['romaji']) 
            
            media.append( {
                "id": data['id'],
                "idMal": f"https://myanimelist.net/anime/{data['idMal']}/",
                "name": data['title']['english'] if data['title']['english'] is not None else data['title']['romaji'],
                "name_format": (data['title']['english']).replace("'","") if data['title']['english'] is not None else (data['title']['romaji']).replace("'",""),
                "romaji": data['title']['romaji'],
                "img_src": data['coverImage']['extraLarge'],
                "airing" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] )  ,
                "airingAt" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] ).strftime( "%Y-%m-%d")  ,
                "airingAt" : datetime.datetime.fromtimestamp( data['nextAiringEpisode']['airingAt'] ).strftime( "%Y-%m-%d")  ,
                "nextAiringEpisode":data['nextAiringEpisode']['episode'],
                "format":data['format'],
                "description":data['description'],
                "hashtag":data['hashtag'],
                "season":data['season'],
                "status":data['status'],
                "episodes":data['episodes'],
                "startDate":data['startDate'],
                "endDate":data['endDate'],
                "sonarr": results
            } )

            #logger(json.dumps(results, indent=4))

        except:
            continue

    
    print(f'page_source => while True  => {datetime.date.today()} ', flush=True)
    print(f"page_source => while True  => {int(datetime.datetime.now().timestamp())} ", flush=True)
    print(f"page_source => while True  => {int(datetime.datetime.now().timestamp()) + int('494325')} ", flush=True)

    
    media_sorted = sorted(
        media, key=lambda x:( x["airing"] is None ,x["airing"] == '' , x["airing"],  x["status"]), reverse=False
    )


    #data = list(dict.fromkeys(data))

    return render_template(
        "index.html",  data=media_sorted,sonarr=respSonarr, root_folders = _root_folders, all_tags = _all_tags, quality_profile_id= _quality_profile_id
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



@index.route("/sonarr")
def seachSonarr():

    search = request.args.get('search', default = 'My Dress-Up Darling', type = str)

    Sonarr = ( sonarr.Sonarr('http://192.168.0.10:8989', '61db77c5ec5b4bc3be57ab3a3f1e36e2') )

    results = Sonarr.lookup_series(search) 


    return json.dumps(results)




@index.route("/add",methods=['POST'])
def add():

    title = request.form.get('title', None)
    apellido = request.form['inputSeries-127050']


    return apellido
    return request.form





@index.route("/update")
def update():

    page = request.args.get('page', default = 1, type = int)
    perPage = request.args.get('perPage', default = 50, type = int)
    year = request.args.get('year', default = datetime.datetime.now().year, type = int)

    database.createTable()
    return 'media_sorted'

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















