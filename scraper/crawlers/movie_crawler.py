class MovieCrawler:
    url = None

    def crawl(self, url):
        self.url = url
        return [url]