import requests
from bs4 import BeautifulSoup

class RWDScanner():

    def __init__(self):
        self.timeout = 5
        self.return_on_error = False

    def scan(self, url):
        response = self._request(url)
        soup = self._get_soup(response)
        self._check_for_viewport(soup)

    def _request(self, url):
        headers = {}
        response = requests.get(url, headers=headers, timeout=self.timeout)
        if self.return_on_error or response.status_code // 100 == 2:
            return response
        return None

    def _get_soup(self, response):
        if response:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        return None

    def _check_for_viewport(self, soup):
        viewports = soup.find_all('meta', {'name': "viewport"})
        for viewport in viewports:
            print(viewport['content'])
            print('device-width' in viewport['content'])

if __name__ == "__main__":
    scanner = RWDScanner()
    scanner.scan('https://www.hkmci.com')