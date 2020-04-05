# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from blogparse.items import AvitoRealEstateItem



class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru', 'avito.ru']
    start_urls = ['https://www.avito.ru/moskva/kvartiry/']

    def parse(self, response):
        for num in response.xpath('//div[@data-marker="pagination-button"]//span/text()'):
            try:
                tmp = int(num.get())
                yield response.follow(f'/moskva/kvartiry/?p={tmp}', callback=self.parse)
            except TypeError as e:
                continue
            except ValueError as e:
                continue

        for ads_url in response.css('div.item_table h3.snippet-title a.snippet-link::attr("href")'):
            yield response.follow(ads_url, callback=self.ads_parse)

    def ads_parse(self, response):
        item = ItemLoader(AvitoRealEstateItem(), response)
        item.add_value('url', response.url)
        item.add_css('title', 'div.title-info-main h1.title-info-title span::text')
        item.add_xpath('photos', "//div[contains(@class, 'gallery-img-frame')]/@data-url")
        item.add_xpath('dpublic', "//div[@class='title-info-metadata-item-redesign']/text()")
        item.add_xpath('floor', "//span[text() = 'Этаж: ']/parent::li/text()[2]")
        item.add_xpath('floorcnt', "//span[text() = 'Этажей в доме: ']/parent::li/text()[2]")
        item.add_xpath('housetype', "//span[text() = 'Тип дома: ']/parent::li/text()[2]")
        item.add_xpath('roomcnt', "//span[text() = 'Количество комнат: ']/parent::li/text()[2]")
        item.add_xpath('square', "//span[text() = 'Общая площадь: ']/parent::li/text()[2]")
        item.add_xpath('kitchensquare', "//span[text() = 'Площадь кухни: ']/parent::li/text()[2]")
        item.add_xpath('buildyear', "//span[text() = 'Год постройки: ']/parent::li/text()[2]")
        item.add_xpath('authorname', '//div[@class="seller-info-name js-seller-info-name"]/a[1]/text()')
        item.add_xpath('authorurl', '//div[@class="seller-info-name js-seller-info-name"]/a[1]/@href')
        yield item.load_item()

