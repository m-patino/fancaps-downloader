from bs4 import BeautifulSoup
from scraper.crawlers import episode_crawler
import re
import urllib.request
import urllib.error
from scraper.utils.colors import Colors

class SeasonCrawler:
    url = None
    name = None

    def crawl(self, url):
        epLinks = []
        picLinks = []
        self.url = url
        currentUrl = self.url
        page = 1

        while currentUrl:
            try:
                request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
                content = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                Colors.print(f"Error occurred while opening the URL: {e.reason}", Colors.RED)
                break
            except urllib.error.HTTPError as e:
                Colors.print(f"HTTP Error: {e.code} {e.reason}", Colors.RED)
                break

            try:
                beautifulSoup = BeautifulSoup(content, 'html.parser')
            except Exception as e:
                Colors.print(f"Error occurred while parsing the page: {e}", Colors.RED)
                break

            for DOMLink in beautifulSoup.find_all('a', class_='btn', href=re.compile("^.*?/episodeimages.php\?")):
                href = DOMLink.get('href')
                if href:
                    if not re.match("^https://.*?/episodeimages.php\?", href):
                        href = 'https://fancaps.net' + DOMLink.get('href')

                    match = re.search(r"https://fancaps.net/.*?/episodeimages.php\?\d+-(.*?)/", href)
                    if match:
                        if not self.name:
                            self.name = match.group(1)
                        if self.name == match.group(1):
                            epLinks.append(href)
            if beautifulSoup.find("a", text=re.compile(r'Next', re.IGNORECASE), href=lambda href: href and href != "#"):
                page += 1
                currentUrl = url + f"&page={page}"
            else:
                currentUrl = None

        crawler = episode_crawler.EpisodeCrawler()
        for epLink in epLinks:
            try:
                episodeResult = crawler.crawl(epLink)
                picLinks.append(episodeResult)
                Colors.print(f"\t{epLink} crawled", Colors.GREEN)
            except Exception as e:
                Colors.print(f"Failed to crawl {epLink}: {e}", Colors.RED)

        return picLinks
