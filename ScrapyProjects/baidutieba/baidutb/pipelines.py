# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BaidutbPipeline:
    def process_item(self, item, spider):
        # client = MongoClient()
        # collection = client['tencent']['hr']
        # collection.insert(item)
        return item
