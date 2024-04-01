from scraper.url_support import UrlSupport
from scraper.crawlers import episode_crawler, season_crawler, movie_crawler

class Crawler:
    def crawl(self, url):
        url = url

        urlSupport = UrlSupport()
        urlType = urlSupport.getType(url)
        if urlType == 'season':
            crawler = season_crawler.SeasonCrawler()
            output = crawler.crawl(url)
        elif urlType == 'episode':
            crawler = episode_crawler.EpisodeCrawler()
            output = [crawler.crawl(url)]
        elif urlType == 'movie':
            crawler = movie_crawler.MovieCrawler()
            output = [crawler.crawl(url)]
        else:
            return []

        return output