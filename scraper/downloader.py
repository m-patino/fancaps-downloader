import os
import threading
import concurrent.futures
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
from tqdm import tqdm
import time
from http.client import IncompleteRead  # IncompleteRead例外をインポート

def _download(url, path, timeout=10, attempts=3, delay=0.01):  # attemptsパラメータを追加
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'})
    filename = os.path.join(path, url.split('/')[-1])

    for attempt in range(attempts):
        try:
            with urlopen(req, timeout=timeout) as response, open(filename, 'wb') as output:
                data = response.read()
                output.write(data)
                break  # ダウンロードに成功したらループを抜ける
        except (HTTPError, URLError, IncompleteRead) as e:
            print(f"ダウンロード中にエラーが発生しました: {e}. 再試行します...({attempt+1}/{attempts})")
            time.sleep(delay)  # エラー後に少し待ってから再試行
        except TimeoutError as e:
            print(f"タイムアウトエラー: {e}. 再試行します...({attempt+1}/{attempts})")
            time.sleep(delay)
        else:
            break  # 他の例外がなければループを抜ける
        if attempt == attempts - 1:
            print(f"エラーによりダウンロードに失敗しました: {url}")

    time.sleep(delay)  # ダウンロードの間隔を空ける

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
                    future = executor.submit(_download, url, path, delay=delay)  # delayを引数として渡す
                    future.add_done_callback(lambda _: update_progress())
                    futures.append(future)

                for future in concurrent.futures.as_completed(futures):
                    future.result()
