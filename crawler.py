from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import sys


class AnchorTagCrawler(object):

    def __init__(self, url_list, threads=1, iterations=1):
        self.keys = ''
        self.urls = [url_list]
        self.max_threads = threads
        self.count = 0
        self.iterations = iterations

    # MAKES CONCURRENT REQUESTS TO GIVEN URL
    @staticmethod
    def make_request(url):

        try:
            r = requests.get(url=url, timeout=20)
            r.raise_for_status()
        except requests.exceptions.Timeout:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.ConnectionError:
            r = requests.get(url=url, timeout=60)
        except requests.exceptions.RequestException as e:
            raise e
        return r.text

    # WRITES CRAWLED OUTPUT TO FILE
    @staticmethod
    def write_to_file(url_text, link_text):

        with open('crawled_urls.txt', 'a') as f:
            f.write(url_text + '\n')

        for link in link_text:
            with open('crawled_urls.txt', 'a') as f:
                f.write('    ' + link + '\n')

    # PARSES URL RESULTS AND CALLS WRITE TO FILE
    def __parse_results(self, url, html):

        links = []

        try:
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                ref = link.get('href').split(':')
                # CREATES LIST OF LINKS
                if ref[0] == 'http' or ref[0] == 'https':
                    links.append(link.get('href'))
        except Exception as e:
            raise e

        self.write_to_file(url, links)

        # ITERATES NEWLY FOUND URLS SET BY ITERATION NUMBER
        if self.count < self.iterations:
            self.crawl_again(links)

    # CRAWLS NEWLY FOUND URLS
    def crawl_again(self, results):

        thread_count = len(results)
        self.max_threads = thread_count
        self.urls = results
        self.count += 1
        self.run_script()

    # REQUESTS HTML TEXT AND CALLS RESULT PARSING
    def wrapper(self, url):

        html = self.make_request(url)
        self.__parse_results(url, html)

    # RUNS SCRIPT
    def run_script(self):

        with ThreadPoolExecutor(max_workers=min(len(self.urls), self.max_threads)) as Executor:
            jobs = [Executor.submit(self.wrapper, u) for u in self.urls]


if __name__ == '__main__':

    input1 = sys.argv[1]

    example = AnchorTagCrawler(input1)

    example.run_script()
