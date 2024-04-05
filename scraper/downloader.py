import os
import threading
import concurrent.futures
from urllib.error import HTTPError,URLError  
from urllib.request import urlopen, Request
from tqdm import tqdm

def _download(url, path, timeout=10):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
    filename = os.path.join(path, url.split('/')[-1])

    try:
        with urlopen(req, timeout=timeout) as response, open(filename, 'wb') as output:
            data = response.read()
            output.write(data)
    except (HTTPError, TimeoutError, URLError) as e:
        return

class Downloader:

    def downloadUrls(self, path, urls):
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
                    future = executor.submit(_download, url, path)
                    future.add_done_callback(lambda _: update_progress())
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    future.result()

    

