import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import os

class EpisodeCrawler:
    def crawl(self, url):
        picLinks = []  # List to store the picture links
        currentUrl = url  # Current URL to crawl
        pageNumber = 1  # Initialize page number
        alt = None  # Initialize alt attribute value for images

        # Extract episode type, subfolder information from URL
        match = re.search(r"https://fancaps.net\/([a-zA-Z]+)\/.*\?\d+-(.*?)/(.*)", url)
        if not match:
            print("Invalid URL format.")
            return {"subfolder": "", "links": []}

        epType = match.group(1)  # Episode type (tv or anime)
        subfolder = os.path.join(match.group(2), match.group(3))  # Construct subfolder path

        # Set CDN based on episode type
        if epType == 'tv':
            cdn = 'tvcdn'
        else:
            cdn = 'ancdn'

        while currentUrl:
            try:
                # Make a request to the current URL
                request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
                page = urllib.request.urlopen(request)
            except urllib.error.URLError as e:
                print(f"Error opening URL: {e.reason}")
                break
            except urllib.error.HTTPError as e:
                print(f"HTTP Error: {e.code} {e.reason}")
                break

            try:
                # Parse the HTML content
                beautifulSoup = BeautifulSoup(page, "html.parser")
            except Exception as e:
                print(f"Error parsing page: {e}")
                break

            # Find all image tags with a specific source pattern
            for img in beautifulSoup.find_all("img", src=re.compile("^https://"+epType+"thumbs.fancaps.net/")):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not alt:
                    alt = imgAlt  # Set alt if not already set
                if alt == imgAlt:
                    # Add image source to list, replacing the domain with the CDN domain
                    picLinks.append(imgSrc.replace("https://"+epType+"thumbs.fancaps.net/", "https://"+cdn+".fancaps.net/"))

            # Check for a next page link
            nextPage = beautifulSoup.find("a", href=lambda href: href and f"&page={pageNumber + 1}" in href)
            if nextPage:
                pageNumber += 1  # Increment page number
                currentUrl = f"{url}&page={pageNumber}"  # Update current URL
            else:
                currentUrl = None  # No more pages, stop crawling

        return {
            'subfolder': subfolder,  # Return subfolder path
            'links': picLinks  # Return list of picture links
        }
