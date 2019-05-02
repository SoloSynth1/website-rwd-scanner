import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class RWDScanner():

    def __init__(self):
        self.timeout = 5
        self.return_on_error = False
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,ja;q=0.8,zh-TW;q=0.7,zh;q=0.6,zh-CN;q=0.5',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36'
            }

    def scan(self, url):
        landing_url = url

        response = self._request(url)
        soup = self._get_soup(response)

        scan_results = {'input_url': url,
                        'landing_url': landing_url,
                        'results': {}}

        if soup:

            landing_url = response.url  # to include cases being redirected

            scan_results['retrieve-success'] = True
            scan_results['response_time'] = response.elapsed.total_seconds()
            scan_results['results']['supports-device-width'] = self._check_for_viewport(soup)
            scan_results['results']['supports-@media-style'] = self._check_stylesheets_for_at_media(soup, landing_url)
            scan_results['results']['contains-ga-gtm-script'] = self._check_for_ga_tags(soup, url)
        else:
            scan_results['retrieve-success'] = False
            scan_results['response_time'] = 0
            scan_results['results']['supports-device-width'] = False
            scan_results['results']['supports-@media-style'] = False
            scan_results['results']['contains-ga-gtm-script'] = False
        return scan_results

    def _request(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            if self.return_on_error or response.status_code // 100 == 2:
                return response
            return None
        except:
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

    def _check_stylesheets_for_at_media(self, soup, url):
        local_stylesheets = self._get_local_stylesheets(soup)
        for local_stylesheet in local_stylesheets:
            if '@media' in local_stylesheet:
                return True
        external_stylesheets = self._get_external_stylesheet_links(soup, url)
        for external_stylesheet in external_stylesheets:
            response = self._request(external_stylesheet)
            if response and '@media' in response.text:
                return True
        return False

    def _get_local_stylesheets(self, soup):
        return [x.text for x in soup.find_all('style')]

    def _get_external_stylesheet_links(self, soup, url):
        return [urljoin(url, x['href']) for x in soup.find_all('link', {'rel': 'stylesheet'}) if x.has_attr('href')]

    def _check_for_ga_tags(self, soup, url):
        scripts = self._get_scripts(soup)
        for script in scripts:
            if script.has_attr('src'):
                response = self._request(urljoin(url, script['src']))
                if response:
                    text = response.text
                else:
                    continue
            else:
                text = script.text
            if 'www.googletagmanager.com' in text or 'www.google-analytics.com' in text:
                return True
        return False

    def _get_scripts(self, soup):
        return [x for x in soup.find_all('script')]


if __name__ == "__main__":
    scanner = RWDScanner()
    print(scanner.scan('https://www.google.com'))