import os
import threading
import concurrent.futures
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from tqdm import tqdm
import time
from http.client import IncompleteRead  # Import IncompleteRead exception

def _download(url, path, timeout=10, attempts=3, delay=0.01):  # Added attempts parameter
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
    filename = os.path.join(path, url.split('/')[-1])

    for attempt in range(attempts):
        try:
            with urlopen(req, timeout=timeout) as response, open(filename, 'wb') as output:
                data = response.read()
                output.write(data)
                break  # Exit the loop if download is successful
        except (HTTPError, URLError, IncompleteRead) as e:
            print(f"An error occurred during download: {e}. Retrying...({attempt+1}/{attempts})")
            time.sleep(delay)  # Wait a bit before retrying after error
        except TimeoutError as e:
            print(f"Timeout Error: {e}. Retrying...({attempt+1}/{attempts})")
            time.sleep(delay)
        else:
            break  # Exit the loop if no other exceptions occur
        if attempt == attempts - 1:
            print(f"Download failed due to errors: {url}")

    time.sleep(delay)  # Pause between downloads

class Downloader:

    def downloadUrls(self, path, urls, delay=1):
        os.makedirs(path, exist_ok=True)

        total = len(urls)
        lock = threading.Lock()

        def update_progress():
            with lock:
                pbar.update(1)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            with tqdm(total=total) as pbar:
                futures = []
                for url in urls:
                    future = executor.submit(_download, url, path, delay=delay)  # Pass delay as an argument
                    future.add_done_callback(lambda _: update_progress())
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    future.result()

