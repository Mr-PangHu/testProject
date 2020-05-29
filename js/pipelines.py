# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from openpyxl import Workbook
import codecs

def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "123456",
        charset = "utf8",
        use_unicode = False
    )
    return conn


class JsPipeline(object):

    def __init__(self):
        self.fp=open("js.json",'w',encoding='utf-8')
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['article_id', 'title', 'author', 'content', 'comment', 'likes', 'authorlink', 'url', 'piclink', 'time'])

    def open_spider(self,spider):
        print('爬虫开始了……')

    def process_item(self, item, spider):
        file_name = item['article_id']
        file_name += ".txt"
        fp1 = codecs.open('C:/Users/13931/Desktop/jianshu' + '/' + file_name, 'w', encoding='utf-8')
        fp1.write(item['artical'])
        fp1.close()

        item_json=json.dumps(dict(item),ensure_ascii=False)
        self.fp.write(item_json+'\n')
        line = [item['article_id'], item['title'][0], item['author'][0], item['content'], item['comment'], item['likes'], item['authorlink'], item['url'], item['piclink'], item['time']]  # 把数据每一行整理出来
        self.ws.append(line)  # 将数据一行的形式添加到xlsx中
        self.wb.save('js.xlsx')  # 保存xlsx文件

        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE websitedb")
        sql = "INSERT INTO new(new_id,new_time,comment,likes,new_title,new_content,author,authorlink,url,piclink) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cursor.execute(sql,
                           (item['article_id'], item['time'], item['comment'], item['likes'], item['title'], item['content'], item['author'],  item['authorlink'], item['url'], item['piclink']))
            cursor.connection.commit()
        except BaseException as e:
            print("article_id重复！", e)
            dbObject.rollback()
        return item



    def close_spider(self,spider):
        self.fp.close()

        print('爬虫结束了……')

