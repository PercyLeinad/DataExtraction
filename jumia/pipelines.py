# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

import scrapy
from itemadapter import ItemAdapter
from itemloaders.processors import TakeFirst, MapCompose, Join, Compose
import re
from dataclasses import dataclass, field

def clean_value(value):
    return value[0].removeprefix('KSh').replace(',', '').strip()
    
class JumiaPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        brand_key = 'brand'
        value = adapter.get(brand_key)
        if value is None:
            adapter[brand_key] =  'No brand'
        else:
            adapter[brand_key] =  value

        adapter['old_price'] = clean_value(adapter.get('old_price', ['0']))
        return item
    
class JumiaSaveToSqlpipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '2961',
            database = 'jumia'
        )
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS smartphones
                        (name text,
                        brand text,
                        new_price int,
                        old_price int )""")
    def process_item(self,item,spider):
        self.cur.execute("""INSERT INTO smartphones(name,brand,new_price,old_price) VALUES(%s,%s,%s,%s)""",(
                        item['name'],
                        item['brand'],
                        item['new_price'],
                        item['old_price']       
                        ))
        self.conn.commit()
        return item
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()

        

