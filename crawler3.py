from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests

class ConcurrentCrawler(object):

    def __init__(self, url_list, threads):

        self.urls = url_list
        self.results = {}
        self.max_threads = threads

    def __make_request(self, url):

        try:
            r = requests.get(url=url, timeout=20)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.ConnectionError:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.RequestException as e:
            raise e
        return r.url, r.text

    def __parse_results(self, url, html):

        try:
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title').get_text()
        except Exception as e:
            raise e

        if title:
            self.results[url] = title

    def wrapper(self, url):
        url, html = self.__make_request(url)
        self.__parse_results(url, html)

    def run_script(self):
        with ThreadPoolExecutor(max_workers=min(len(self.urls),self.max_threads)) as Executor:
            jobs = [Executor.submit(self.wrapper, u) for u in self.urls]


if __name__ == '__main__':




    example = ConcurrentCrawler(['http://edmundmartin.com',
                                     'https://www.udemy.com',
                                     'https://github.com/',
                                     'https://pirateproxy.cc',
                                     'https://www.facebook.com/'],5)
    example.run_script()
    print(example.results)