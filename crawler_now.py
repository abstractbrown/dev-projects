from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests


class ConcurrentCrawler(object):

    def __init__(self, url_list, threads=1, iterations=1):
        self.keys = ''
        self.urls = url_list
        self.max_threads = threads
        self.count = 0
        self.iterations = iterations

    @staticmethod
    def __make_request(url):

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

    # PARSES URL RESULTS
    def __parse_results(self, url, html):
        self.links = []

        try:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                ref = link.get('href').split(':')
                # CREATES LIST OF LINKS
                if ref[0] == 'http' or ref[0] == 'https':
                    self.links.append(link.get('href'))
        except Exception as e:
            raise e

        # WRITES OUTPUT TO FILE
        with open('crawled_urls.txt', 'a') as f:
            f.write(url + '\n')

        for l in self.links:
            with open('crawled_urls.txt', 'a') as f:
                f.write('    ' + l + '\n')

        # ITERATES NEWLY FOUND URLS SET BY ITERATION NUMBER
        if self.count < self.iterations:
            self.__crawl_again(self.links)

    # CRAWLS NEWLY FOUND URLS
    def __crawl_again(self, results):
        thread_count = len(results)
        self.max_threads = thread_count
        self.urls = results
        self.count += 1
        self.run_script()

    # FIRES OFF INITIAL PARSING
    def wrapper(self, url):
        print('THis URL' + url)
        url, html = self.__make_request(url)
        self.__parse_results(url, html)

    # RUNS SCRIPT
    def run_script(self):
        with ThreadPoolExecutor(max_workers=min(len(self.urls), self.max_threads)) as Executor:
            jobs = [Executor.submit(self.wrapper, u) for u in self.urls]


if __name__ == '__main__':

    example = ConcurrentCrawler(['http://www.rescale.com'])

    example.run_script()
