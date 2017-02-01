import time
import threading
from download import Downloader
SLEEP_TIME = 1

def threaded_crawler(max_threads = 10):
    # urls that still need to be crawled
    crawl_queue = [seed_url]
    # urls that have been seen
    seen = set([seed_url])
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    def proxess_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # empty queue
                break
            else:
                html = D(url)
                threads = []
                while threads or crawl_queue:
                    for thread in threads:
                        if not thread.is_alive():
                            threads.remove(thread)
                    while len(threads) < max_threads and crawl_queue:
                        # can start some more threads
                        thread = threading.Tread(target=proxess_queue)
                        thread.setDaemon(True)
                        thread.start()
                        threads.append(thread)

                    time.sleep(SLEEP_TIME)