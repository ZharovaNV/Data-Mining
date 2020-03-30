# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class BlogparseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def clean_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


class AvitoRealEstateItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(clean_photo))
    dpublic = scrapy.Field(output_processor=TakeFirst())
    floor = scrapy.Field(output_processor=TakeFirst())
    floorcnt = scrapy.Field(output_processor=TakeFirst())
    housetype = scrapy.Field(output_processor=TakeFirst())
    roomcnt = scrapy.Field(output_processor=TakeFirst())
    square = scrapy.Field(output_processor=TakeFirst())
    kitchensquare = scrapy.Field(output_processor=TakeFirst())
    buildyear = scrapy.Field(output_processor=TakeFirst())
    authorname = scrapy.Field(output_processor=TakeFirst())
    authorurl = scrapy.Field(output_processor=TakeFirst())
