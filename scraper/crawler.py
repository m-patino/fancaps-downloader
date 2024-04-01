from scraper.url_support import UrlSupport
from scraper.crawlers import episode_crawler, season_crawler, movie_crawler

class Crawler:
    url = None
    urlType = None

    def crawl(self, url):
        self.url = url

        urlSupport = UrlSupport()
        self.urlType = urlSupport.getType(self.url)
        if self.urlType == 'season':
            crawler = season_crawler.SeasonCrawler()
        elif self.urlType == 'episode':
            crawler = episode_crawler.EpisodeCrawler()
        elif self.urlType == 'movie':
            crawler = movie_crawler.MovieCrawler()
        else:
            return []

        return crawler.crawl(self.url)