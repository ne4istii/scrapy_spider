import base64
import json
from urllib.parse import urljoin

import scrapy

import free_proxy_scraper.settings as s


class ProxySpider(scrapy.Spider):
    name = 'proxy'
    start_urls = [s.FREE_PROXY_URL]
    page_counter = 0
    results = {}

    def parse(self, response):
        self.proxies = []
        proxy_table_tr = response.xpath('//table[@id="proxy_list"]/tbody/tr')
        for tr in proxy_table_tr:
            tds = tr.xpath('./td')
            try:
                selector = './/script[@type="text/javascript"]/text()'
                re_pattern = r'\"([a-zA-Z0-9=\/+]*)\"'
                ip_addr_b64 = tds[0].xpath(selector).re(re_pattern)
                ip_addr = base64.b64decode(f'{ip_addr_b64}').decode('utf-8')
                port = tds[1].xpath('./span/text()').get()
                self.proxies.append(f'{ip_addr}:{port}')
            except Exception as e:
                pass
        self.page_counter += 1
        self.next_page = response.css('link[rel="next"]').attrib['href']
        url = urljoin(s.UPLOAD_PROXY_URL, s.API_GET_TOKEN_METHOD)
        yield scrapy.Request(
            url=url, method='GET', headers=s.UPLOAD_HEADERS,
            callback=self.upload_proxy, dont_filter=True)

    def upload_proxy(self, response):
        payload = {
            'user_id': s.USER_ID_TOKEN,
            'len': len(self.proxies),
            'proxies': ', '.join(self.proxies)
        }
        url = urljoin(s.UPLOAD_PROXY_URL, s.API_POST_PROXIES_METHOD)
        yield scrapy.Request(
            url=url, method='POST', body=json.dumps(payload),
            headers=s.UPLOAD_HEADERS, callback=self.save_proxies_json,
            dont_filter=True)

    def save_proxies_json(self, response):
        data = json.loads(response.body)
        save_id = data.get('save_id', False)
        if save_id:
            self.results.update({save_id: self.proxies})
        if (self.next_page is not None and 
                self.page_counter < s.PARSE_PAGE_COUNTER):
            yield response.follow(
                urljoin(s.FREE_PROXY_URL, self.next_page),
                self.parse, dont_filter=True)
        else:
            yield self.results
