import re
from bs4 import BeautifulSoup
import urllib.request

class EpisodeCrawler:
    url = None
    alt = None

    def crawl(self, url):
        picLinks = []
        self.url = url
        currentUrl = self.url
        pageNumber = 1

        # get Episode type for setup  cdn and regex
        match = re.search(r"https://fancaps.net/(.*?)/(.*)", url)
        epType = match.group(1)
        nextUrl = match.group(2)

        if epType == 'tv':
            cdn = 'tvcdn'
        else:
            cdn = 'ancdn'

        while currentUrl:
            request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
            page = urllib.request.urlopen(request)
            beautifulSoup = BeautifulSoup(page, "html.parser")

            for img in beautifulSoup.find_all("img", src=re.compile("^https://"+epType+"thumbs.fancaps.net/")):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not self.alt:
                    self.alt = imgAlt
                if self.alt == imgAlt:
                    picLinks.append(imgSrc.replace("https://"+epType+"thumbs.fancaps.net/", "https://"+cdn+".fancaps.net/"))
            next = nextUrl+f"&page={pageNumber + 1}"
            nextPage = beautifulSoup.find("a", href=next)
            if nextPage:
                pageNumber += 1
                currentUrl = url + f"&page={pageNumber}"
            else:
                currentUrl = None
        
        return picLinks