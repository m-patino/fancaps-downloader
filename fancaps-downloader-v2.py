import argparse
from scraper.crawler import Crawler
from scraper.downloader import Downloader
import os

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', help='Url to start download')
parser.add_argument('--output', type=str, default="Downloads", help='Path of folder')
args = parser.parse_args()

if __name__ == "__main__":
    # Crawl
    crawler = Crawler()
    links = crawler.crawl(args.url)

    # Download
    downloader = Downloader()
    for item in links:
        path = os.path.join(args.output, item['subfolder'])
        downloader.downloadUrls(path, item['links'])