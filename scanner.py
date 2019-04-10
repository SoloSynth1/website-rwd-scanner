import requests
from bs4 import BeautifulSoup

class RWDScanner():

    def __init__(self):
        self.timeout = 5
        self.return_on_error = False
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8,zh-TW;q=0.7,zh;q=0.6,zh-CN;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
            }

    def scan(self, url):
        response = self._request(url)
        soup = self._get_soup(response)

        scan_results = {'url': url,
                        'results': {}}
        if soup:
            scan_results['retrieve-sucess'] = True
            scan_results['results']['supports-device-width'] = self._check_for_viewport(soup)
        else:
            scan_results['retrieve-sucess'] = False
        return scan_results

    def _request(self, url):
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
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
            if 'device-width' in viewport['content']:
                return True
        return False

    def _get_stylesheets(self, soup):
        stylesheets = soup.find_all('')

if __name__ == "__main__":
    scanner = RWDScanner()
    print(scanner.scan('https://goodad.co'))