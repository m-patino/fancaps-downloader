import re
from bs4 import BeautifulSoup
import urllib.request

class MovieCrawler:
    def crawl(self, url):
        picLinks = []
        currentUrl = url
        pageNumber = 1
        alt = None

        try:
            # Extract subfolder name from URL
            match = re.search(r"https://fancaps.net\/.*\?name=(.*)&", url)
            if match:
                subfolder = match.group(1)
            else:
                raise ValueError("URL does not contain a valid subfolder name.")
        except ValueError as e:
            print(f"Error extracting subfolder: {e}")
            return

        while currentUrl:
            try:
                # Fetch and parse the webpage
                request = urllib.request.Request(currentUrl, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
                page = urllib.request.urlopen(request)
                beautifulSoup = BeautifulSoup(page, "html.parser")
            except Exception as e:
                print(f"Error fetching or parsing page: {e}")
                break
            
            for img in beautifulSoup.find_all("img", src=re.compile("^https://moviethumbs.fancaps.net/")):
                imgSrc = img.get("src")
                imgAlt = img.get("alt")
                if not alt:
                    alt = imgAlt
                if alt == imgAlt:
                    picLinks.append(imgSrc.replace("https://moviethumbs.fancaps.net/", "https://mvcdn.fancaps.net/"))
            
            try:
                # Generate and verify the existence of the next page URL
                next = url.replace(f'https://fancaps.net/movies/','') +f"&page={pageNumber + 1}"
                nextPage = beautifulSoup.find("a", href=next)
                if nextPage:
                    pageNumber += 1
                    currentUrl = url + f"&page={pageNumber}"
                else:
                    currentUrl = None
            except Exception as e:
                print(f"Error processing next page: {e}")
                break
        
        return {
            'subfolder': subfolder,
            'links': picLinks
        }
