import scrapy
import json
import time


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent_hr.com']
    start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1598369543278&countryId=&'
                  'cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex=1&'
                  'pageSize=10&language=zh-cn&area=cn']

    def parse(self, response):
        # print(response.text)
        data = json.loads(response.text)
        data_list = data['Data']['Posts']
        for item in data_list:
            item.pop('Id')
            item.pop('PostId')
            item.pop('RecruitPostId')
            item.pop('SourceID')
            item.pop('IsCollect')
            item.pop('IsValid')
            yield item

        total_page = data['Data']['Count'] / 10
        urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={0}&countryId='
                '&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&'
                'pageIndex={1}&pageSize=10&language=zh-cn&area=cn'.format(time.time(), i) for i in
                range(1, int(total_page) + 1)]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
