import scrapy
import urllib
from copy import deepcopy


class TbSpider(scrapy.Spider):
    name = 'tb'
    allowed_domains = ['baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=steam']

    def parse(self, response):
        # 置顶贴分组
        top_list = response.xpath('//div[@class="t_con cleafix"]')
        for top in top_list:
            item = {
                "title": top.xpath('./div[2]/div/div/a/text()').extract_first(),
                'href': top.xpath('./div[2]/div/div/a/@href').extract_first(),

            }
            if item['href'] is not None:
                item['href'] = urllib.parse.urljoin(response.url, item['href'])
                yield scrapy.Request(
                    item['href'],
                    callback=self.parse_detail,
                    meta={'item': deepcopy(item)}
                )
        next_page = response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            next_page = urllib.parse.urljoin(response.url, next_page)
            yield scrapy.Request(
                next_page,
                callback=self.parse
            )

    def parse_detail(self, response):
        item = response.meta['item']
        # div_list = response.xpath('//div[@class="p_postlist"]/div')
        # for div in div_list:
        #     floor = div.xpath('.//span[@class="tail-info"]/text()').extract()[-2]
            # print(floor)
            # item[floor] = {
            #     'author':
            #         div.xpath('./div[@class="d_author"]/ul/li[@class="d_name"]/a/text()').extract_first(),
            #     "user_id":
            #         eval(div.xpath('./div[@class="d_author"]/ul/li[@class="d_name"]/@data-field').extract_first())["user_id"],
            #     "badge_title":
            #         div.xpath('./div[@class="d_author"]/ul/li[@class="l_badge"]/div/a/div[1]/text()').extract_first(),
            #     "badge_level":
            #         div.xpath('./div[@class="d_author"]/ul/li[@class="l_badge"]/div/a/div[2]/text()').extract_first(),
            #     "content":
            #         [i.strip() for i in div.xpath('./div[2]/div[@class="p_content  "]/cc/div[2]//text()').extract() if i],
            #     "img": div.xpath('./div[2]/div[@class="p_content  "]/cc/div[2]/img/@src').extract(),
            #     'post_time': div.xpath('.//span[@class="tail-info"]/text()').extract()[-1]
            # }

        print(item)
        # yield item
        # next_page = response.xpath("//a[text()='下一页']/@href").extract_first()
        #
        # if next_page is not None:
        #     next_page = urllib.parse.urljoin(response.url, next_page)
        #     yield scrapy.Request(
        #         next_page,
        #         callback=self.parse_detail
        #     )
