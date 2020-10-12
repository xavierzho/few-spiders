import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['allitebooks.com']
    start_urls = ['http://www.allitebooks.com/']
    base_url = 'http://www.allitebooks.com/page/{}/'

    def parse(self, response):

        # 所有的书本url
        book_list = response.xpath('//div[@class="entry-body"]/header')
        item = {}
        total_page = int(response.css('.pages ::text').extract_first().split(' ')[2])
        current_page = int(response.css('.pages ::text').extract_first().split(' ')[0])

        for book in book_list:
            item['Book_name'] = book.xpath('./h2/a/text()').extract_first()
            item['Book_url'] = book.xpath('./h2/a/@href').extract_first()
            if item['Book_url'] is not None:
                yield scrapy.Request(
                    url=item['Book_url'],
                    callback=self.parse_detail,
                    dont_filter=False,
                    meta={'item': item})
        if total_page >= current_page:
            yield scrapy.Request(
                self.base_url.format(current_page + 1),
                callback=self.parse,
                dont_filter=False
            )

    def parse_detail(self, response):
        item = response.meta['item']

        item['Author'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[1]//text()').extract())
        item['ISBN-10'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[2]//text()').extract())
        item['Year'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[3]//text()').extract())
        item['Pages'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[4]//text()').extract())
        item['Language'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[5]//text()').extract())
        item['Category'] = ''.join(response.xpath('//div[@class="book-detail"]/dl/dd[8]//text()').extract())
        item['Book_description'] = ''.join(response.xpath('//div[@class="entry-content"]//text()').extract()).replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()
        yield item
