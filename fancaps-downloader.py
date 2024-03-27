import argparse
import re
import urllib.request
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', help='Url to start download')
args = parser.parse_args()

def getUrlType(url):
    match = re.search(r"https://fancaps.net/(.*?)/showimages.php.*?",url)
    if match:
        return "season"
    match = re.search(r"https://fancaps.net/(.*?)/episodeimages.php.*?",url)
    if match:
        return "ep"
    match = re.search(r"https://fancaps.net/movies/MovieImages.php.*?",url)
    if match:
        return 'movie'

def getSeasonLinks(url):
    links = []
    currentUrl = url
    pageNumber = 1
    name = None

    while currentUrl:
        request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0'})
        page = urllib.request.urlopen(request)
        beautifulSoup = BeautifulSoup(page, 'html.parser')

        for link in beautifulSoup.find_all("a", href=re.compile("^.*?/episodeimages.php\?")):
            href = link.get('href')
            if href:
                match = re.search(r"https://fancaps.net/.*?/episodeimages.php\?\d+-(.*?)/", href)
                if match:
                    if not name:
                        name = match.group(1)
                    if name == match.group(1):
                        links.append(href)
        if beautifulSoup.find("a", title="Next Page"):
            pageNumber += 1
            currentUrl = url + f"&page={pageNumber}"
        else:
            currentUrl = None  
    return links


if args.url:
    type = getUrlType(args.url)
    if type == "season":
        for epUrl in getSeasonLinks(args.url):
            print(epUrl)
    elif type == "ep":
        print(type)
    elif type == "movie":
        print(type)
    else:
        print("Invalid url")
