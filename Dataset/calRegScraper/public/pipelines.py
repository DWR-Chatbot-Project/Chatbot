# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Tutorials: 
# https://www.mongodb.com/basics/how-to-use-mongodb-to-store-scraped-data
# https://medium.com/@jebaseelanravi96/scrapy-tutorial-part-4-e363793d4c94

import os
import sys
import urllib.parse

import pymongo
from dotenv import load_dotenv

from .items import Regulation

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


load_dotenv()

class RulescraperPipeline:

    collection = 'regItems'

    # you can also enter your credentials from command line
    # def __init__(self, mongodb_uri, mongodb_db):
    #     self.mongodb_uri = mongodb_uri
    #     self.mongodb_db = mongodb_db
    #     if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")
    
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongodb_uri=crawler.settings.get('MONGODB_URI'),
    #         mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
    #     )
    
    def open_spider(self, spider):
        # self.client = pymongo.MongoClient(self.mongodb_uri)
        self.client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        print("Connecting to: ", os.getenv("MONGODB_URI"))
        # self.db = self.client[self.mongodb_db]
        self.db = self.client[os.getenv("MONGODB_DATABASE")]
        # start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(Regulation(item))
        self.db[self.collection].insert_one(data)
        return item
