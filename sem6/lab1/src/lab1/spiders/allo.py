# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.http.response import Response


class AlloSpider(scrapy.Spider):
    name = 'allo'
    allowed_domains = ['allo.ua']
    start_urls = ['https://allo.ua/ua/velosipedy/']

    def start_requests(self):  #was a mistake without it (INFO: Ignoring response <403 https://allo.ua/ua/velosipedy/>: HTTP status code is not handled or not allowed)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url, headers=headers)

    def parse(self, response: Response):
        products = response.xpath("//ul[(contains(@class, 'products-grid'))]/li[contains(@class, 'item')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//a[contains(@class, 'product-name')]/span/text()[1]").get(),
                'price': product.xpath(".//span[contains(@class, 'new_sum')]/text()[1]").get(),
                'img': product.xpath(".//img/@src").get()
            }
