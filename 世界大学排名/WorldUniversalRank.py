import requests
from lxml import etree


class RankSpider(object):
    def __init__(self):
        self.university_information = []
        self.url = "http://www.zuihaodaxue.com/subject-ranking/computer-science-engineering.html"

    def getHtmlText(self, url):
        # 获取页面内容
        try:
            r = requests.get(url, timeout=30)
            # print(r.status_code)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            return e

    def fillUniversistyList(self, html):

        xpath_data = etree.HTML(html)
        # // *[ @ id = "UniversityRanking"] / tbody / tr[1] / td[3] / img
        rank_data = xpath_data.xpath("//td[1]/text()")
        school_name = xpath_data.xpath("//td[2]/text()")
        country_data = xpath_data.xpath("//td[3]/img/@title")
        countrt_rank = xpath_data.xpath("//td[4]/text()")
        total_score = xpath_data.xpath("//td[5]/text()")
        index_one = xpath_data.xpath("//td[6]/text()")
        inder_two = xpath_data.xpath("//td[7]/text()")
        index_three = xpath_data.xpath("//td[8]/text()")
        index_four = xpath_data.xpath("//td[9]/text()")
        index_five = xpath_data.xpath("//td[10]/text()")
        university_list = zip(rank_data,
                              school_name,
                              country_data,
                              countrt_rank,
                              total_score,
                              index_one,
                              inder_two,
                              index_three,
                              index_four,
                              index_five
                              )

        for i in university_list:
            str1 = ' '.join(i)
            print(str1)

    def main(self):

        html = self.getHtmlText(self.url)
        self.fillUniversistyList(html)


RankSpider().main()
