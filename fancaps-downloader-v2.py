import argparse
from scraper.crawler import Crawler

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='?', help='Url to start download')
parser.add_argument('--output', type=str, default="Downloads", help='Path of folder')
args = parser.parse_args()

if __name__ == "__main__":
    crawler = Crawler()
    links = crawler.crawl(args.url)
    #for link in links:
    #    print(link)

    print(len(links))