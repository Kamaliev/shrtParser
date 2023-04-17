# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from database.database import Database


class ShortparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

if __name__ == '__main__':
    db = Database()
