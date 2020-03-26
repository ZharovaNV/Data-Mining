# -*- coding: utf-8 -*-
import scrapy
import datetime


class HabrBlogSpider(scrapy.Spider):
    name = 'habr_blog'
    allowed_domains = ['habr.com']
    start_urls = ['https://habr.com/ru/top/weekly/']

    def parse(self, response):
        pagination_urls = response.css('a.toggle-menu__item-link_pagination::attr("href")').extract()
        print(response.url)
        for itm in pagination_urls:
            yield response.follow(itm, callback=self.parse)

        for post_url in response.css('h2.post__title a::attr("href")'):
            yield response.follow(post_url, callback=self.post_parse)

    def post_parse(self, response):
        now = datetime.datetime.now()
        data = {
            'title': response.css('.post__title-text::text').extract_first(),
            'url': response.url,
            'writer': {
                'name': response.xpath('//div[1]/header/a/span[2]/text()').extract_first(),
                'url': response.xpath('//div[1]/header/a/@href').extract_first()
            },
            'comment_cnt': response.xpath('//span[@id="comments_count"]/text()').extract_first().replace('\n','').strip(),
            'post_time': response.xpath('//span[@class="post__time"]/text()').extract_first(),
            'tags': response.xpath('//a[@class = "inline-list__item-link post__tag  "]/text()').extract(),
            'hubs': response.xpath('//a[@class = "inline-list__item-link post__tag"]/text()').extract(),
            'admdate': now.strftime("%d-%m-%Y %H:%M")
        }

        yield data


