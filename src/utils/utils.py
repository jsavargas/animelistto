import requests
import base64
import re

import utils.env as env
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By



def getList():


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


def getSeasonAnimeList(page=1,perPage=50,seasonYear=2022):


    season = setSeasonFields()
    seasonYear = seasonYear if seasonYear else setYearFields()
    
    '''
    TODO: season

    WINTER
    Months December to February

    SPRING
    Months March to May

    SUMMER
    Months June to August

    FALL
    Months September to November
    '''

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
                media(type: ANIME, seasonYear: %d, season: %s, format: TV, sort: [TRENDING_DESC, STATUS]) {
                id
                idMal
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
    ''' % (2022, 'WINTER')

    variables = {
        'page': page,
        'perPage': perPage
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    return response

def getYearAnimeList(page=1,perPage=50,year=2022):


    season = setSeasonFields()
    seasonYear = year if year else setYearFields()


    '''
    TODO: season

    WINTER
    Months December to February

    SPRING
    Months March to May

    SUMMER
    Months June to August

    FALL
    Months September to November
    '''

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
                media(type: ANIME, seasonYear: %d, season: %s, format: TV, sort: [TRENDING_DESC, STATUS]) {
                id
                idMal
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
    ''' % (seasonYear, season)

    variables = {
        'page': page,
        'perPage': perPage
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    return response


def setSeasonFields():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    match currentMonth:
        case 12 | 1 | 2:
            return 'WINTER'
        case 3 | 4 | 5:
            return 'SPRING'
        case 6 | 7 | 8:
            return 'SUMMER'
        case 9 | 10 | 11:
            return 'FALL'

def setYearFields():
    currentDay = datetime.now().day
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    return currentYear
