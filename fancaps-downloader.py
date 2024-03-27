import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', help='Url to start download')
args = parser.parse_args()

def getUrlType(url):
    match = re.search(r"https://fancaps.net/(.*?)/showimages.php.*?",url)
    if match:
        return "season_"+match.group(1)
    match = re.search(r"https://fancaps.net/(.*?)/episodeimages.php.*?",url)
    if match:
        return "ep_"+match.group(1)
    match = re.search(r"https://fancaps.net/movies/MovieImages.php.*?",url)
    if match:
        return 'movie'

type = getUrlType(args.url)
