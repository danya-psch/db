# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.response import Response


class IgotoworldSpider(scrapy.Spider):
    name = 'igotoworld'
    allowed_domains = ['ua.igotoworld.com']
    start_urls = ['https://ua.igotoworld.com/ua/news_list/news.htm']

    def parse(self, response: Response):
        all_images = response.xpath("//img/@src[starts-with(., 'http')]")
        all_text = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()"
        )
        yield {
            'url': response.url,
            'payload': [
                           {
                               'type': 'text',
                               'data': text.get().strip()
                           } for text in all_text
                       ] +
                       [
                           {
                               'type': 'image',
                               'data': image.get()
                           } for image in all_images
                       ]
        }
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., 'https://ua.igotoworld.com/')][substring(., string-length() - 3) = '.htm']"
            )
            selected_links = [link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)
