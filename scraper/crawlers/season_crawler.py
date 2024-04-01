import urllib.request
import re
from bs4 import BeautifulSoup
from scraper.crawlers import episode_crawler

class SeasonCrawler:
    url = None
    name = None

    def crawl(self, url):
        epLinks = []
        links = []
        self.url = url
        currentUrl = self.url
        page = 1

        while currentUrl:
            request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
            content = urllib.request.urlopen(request)
            beautifulSoup = BeautifulSoup(content, 'html.parser')

            for DOMLink in beautifulSoup.find_all('a',class_='btn', href=re.compile("^.*?/episodeimages.php\?")):
                href = DOMLink.get('href')
                if href:
                    # If href don't have protocole and domain name add it
                    if not re.match("^https://.*?/episodeimages.php\?", href):
                        href = 'https://fancaps.net' + DOMLink.get('href')

                    # Get Season name for get Only here links
                    match = re.search(r"https://fancaps.net/.*?/episodeimages.php\?\d+-(.*?)/", href)
                    if match:
                        if not self.name:
                            self.name = match.group(1)
                        if self.name == match.group(1):
                            epLinks.append(href)
            if beautifulSoup.find("a", title="Next Page"):
                page += 1
                currentUrl = url + f"&page={page}"
            else:
                currentUrl = None  
        
        crawler = episode_crawler.EpisodeCrawler()
        for epLink in epLinks:
            links.extend(crawler.crawl(epLink))
        return links