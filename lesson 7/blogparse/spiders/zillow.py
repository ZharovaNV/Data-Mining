# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from blogparse.items import ZillowItem
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    start_urls = ['https://www.zillow.com/san-francisco-ca/']

    browser = webdriver.Firefox()

    def parse(self, response):
        for page_url in response.xpath('//nav[@aria-label="Pagination"]/ul/li/a/@href'):
            yield response.follow(page_url, callback=self.parse)

        for ads_url in response.xpath('//div[@class="list-card-info"]/a/@href'):
            yield response.follow(ads_url, callback=self.ads_parse)
        print(1)

    def ads_parse(self, response):
        item = ItemLoader(ZillowItem(), response)
        self.browser.get(response.url)
        media_col = self.browser.find_element_by_css_selector('.ds-media-col')
        photo_media_len = len(
            self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
        )
        while True:
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            media_col.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
            tmp = len(
                self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
            )

            if tmp == photo_media_len:
                break

            photo_media_len = tmp

        images = [
            itm.get_attribute('srcset').split(' ')[-2] for itm in
            self.browser.find_elements_by_xpath('//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
        ]

        item.add_value('url', response.url)
        item.add_xpath('title', '//head/title/text()')
        item.add_xpath('price', '//h3[@class="ds-price"]/span/span/text()')
        item.add_xpath('address', '//header/h1[@class="ds-address-container"]/span/text()')
        item.add_xpath('sqft', '/html/body/div[1]/div[7]/div[1]/div[1]/div/div/div[3]/div/div/div/div[3]/div[4]/div[1]/div/div[1]/div/div/header/h3/span[4]/span[1]/text()')
        item.add_value('photos', images)
        yield item.load_item()