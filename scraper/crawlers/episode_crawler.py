import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os

class EpisodeCrawler:
    def crawl(self, url):
        picLinks = []
        currentUrl = url
        pageNumber = 1
        alt = None

        # get Episode type for setup cdn and regex
        match = re.search(r"https://fancaps.net\/([a-zA-Z]+)\/.*\?\d+-(.*?)/(.*)", url)
        if not match:
            print("URL形式が無効です。")
            return {"subfolder": "", "links": []}

        epType = match.group(1)
        subfolder = os.path.join(match.group(2), match.group(3))

        if epType == 'tv':
            cdn = 'tvcdn'
        else:
            cdn = 'ancdn'

        while currentUrl:
            try:
                request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
                page = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                print(f"URLを開く際にエラーが発生しました: {e.reason}")
                break
            except urllib.error.HTTPError as e:
                print(f"HTTPエラー: {e.code} {e.reason}")
                break

            try:
                beautifulSoup = BeautifulSoup(page, "html.parser")
            except Exception as e:
                print(f"ページの解析中にエラーが発生しました: {e}")
                break

            for img in beautifulSoup.find_all("img", src=re.compile("^https://"+epType+"thumbs.fancaps.net/")):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not alt:
                    alt = imgAlt
                if alt == imgAlt:
                    picLinks.append(imgSrc.replace("https://"+epType+"thumbs.fancaps.net/", "https://"+cdn+".fancaps.net/"))

            nextPage = beautifulSoup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
            if nextPage:
                pageNumber += 1
                currentUrl = f"{url}&page={pageNumber}"
            else:
                currentUrl = None

        return {
            'subfolder': subfolder,
            'links': picLinks
        }
