# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from database.database import Database


class ShortparserPipeline:
    def __init__(self):
        self.db = Database()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        q = 'insert into "Article"(url, "desc", file) values (?, ?, ?)'
        self.db.execute(q, item['url'], item['desc'], item['pdf'])
        return item
