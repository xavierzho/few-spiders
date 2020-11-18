import scrapy
from copy import deepcopy
from scrapy_splash import SplashRequest


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = ['https://pjapi.jd.com/book/sort?source=bookSort']
    headers = {
        'Referer': 'https://book.jd.com/booksort.html'
    }
    lua_scripts = """
    function main(splash)
        splash:go(splash.args.url)
        splash:wait(1)
        splash:runjs("document.getElementsByClassName('page clearfix')[0].scrollIntoView(true)")
        splash:wait(1)
        return splash:html()
    end
    """

    def start_requests(self):

        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    def parse(self, response):
        html = response.body.decode()
        data = eval(html)
        item = {}
        # print(data)
        for i in data['data']:
            item['f_cate_id'] = str(int(i['fatherCategoryId']))
            item['cate_id'] = str(int(i['categoryId']))
            item['cate_name'] = i['categoryName']
            for i1 in i['sonList']:
                item['s_cate_id'] = str(int(i1['categoryId']))
                item['s_cate_name'] = i1['categoryName']
                item['s_cate_cat'] = 'https://list.jd.com/list.html?cat=' + ",".join(
                    [str(int(i['fatherCategoryId'])), str(int(i['categoryId'])), str(int(i1['categoryId']))])
                yield SplashRequest(item['s_cate_cat'],
                                    callback=self.parse_book_list,
                                    endpoint='execute',
                                    args={"lua_source": self.lua_scripts},
                                    # cache_args=['lua_source'],
                                    headers=self.headers,
                                    meta={'item': deepcopy(item)}
                                    )

    def parse_book_list(self, response):
        item = response.meta['item']
        div_list = response.xpath('//div[@class="gl-i-wrap"]')
        for div in div_list:
            item['book_info'] = {
                'name': div.xpath('./div[@class="p-name"]/a/em/text()').extract_first(),
                'introduction': div.xpath('./div[@class="p-name"]/a/i/text()').extract_first(),
                'author': div.xpath('./div[@class="p-bookdetails"]/span[@class="p-bi-name"]/a/text()').extract_first(),
                'price': ''.join(div.xpath('./div[@class="p-price"]/strong//text()').extract()).strip(),
                'publisher': div.xpath(
                    './div[@class="p-bookdetails"]/span[@class="p-bi-store"]/a/text()').extract_first(),
                'publish_date': div.xpath(
                    './div[@class="p-bookdetails"]/span[@class="p-bi-date"]/text()').extract_first(),
                # 'book_img': 'https' + div.xpath('./div[@class="p-img"]/a/img/@src').extact_first(),
                'book_url': div.xpath('./div[@class="p-name"]/a/@href').extract_first()
            }
            print(item)
            # yield item

        # for page in range(2, 101):
        #     url = response.url + '&page={}'.format(page)
        #     yield scrapy.Request(url, callback=self.parse_book_list, headers=self.headers)
