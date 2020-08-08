# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ToscrapespiderPipeline(object):
    def process_item(self, item, spider):
        """
        这个函数就是管道中 处理子数据的
        :param item: 爬虫文件返回的数据
        :param spider: 这个数据是那个爬虫采集的
        :return: 必须返回下一个管道
        """
        with open(f"{spider.name}.txt", 'a', encoding='utf-8') as fp:
        fp.write(data+'\n')
        return item
