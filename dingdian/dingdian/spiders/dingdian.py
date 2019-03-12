# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request #跟进url
from dingdian.items import DingdianItem

class DingdianSpider(scrapy.Spider):
    count = 0
    name = 'dingdian'
    allowed_domains = ['www.23us.so']
    bash_urls = 'https://www.23us.so/list/'
    bashurl = '.html'
    #https://www.23us.so/list/1_1.html
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    def start_requests(self):
        for i in range(1, 10):
            url = self.bash_urls + str(i) + '_1' + self.bashurl
            yield Request(url, self.parse, headers=self.headers)

        #yield Request('https://www.23us.so/full.html', self.parse, headers=self.headers)

    def parse(self, response):
        max_num = response.xpath('//div[@class = "pagelink"]/a[@class="last"]/text()').extract_first().strip()
        bashurl = str(response.url)[:-7]
        print(response.url)
        for i in range(1, int(max_num)+1):
            url = bashurl + '_' + str(i) + self.bashurl
            yield Request(url, self.get_name, headers=self.headers)

    def get_name(self, response):
        tds = response.xpath('//tr[@bgcolor = "#FFFFFF"]/td[1]')
        #print(tds.extract())
        for td in tds:
            novelurl = td.xpath('./a/@href').extract_first().strip() #小说详情页连接
            novelname = td.xpath('./a/text()').extract_first().strip()#小说名称
            #print(novelurl, novelname)
            yield Request(novelurl, callback=self.get_chapterurl, headers=self.headers, meta={'name':novelname, 'url':novelurl})

    def get_chapterurl(self, response):
        item = DingdianItem()
        item['name'] = response.meta['name']
        item['novelurl'] = response.meta['url']
        item['author'] = response.xpath('//tr[1]/td[2]/text()').extract_first().strip()
        item['serialstatus'] = response.xpath('//tr[1]/td[3]/text()').extract_first().strip()
        item['serialnum'] = response.xpath('//tr[2]/td[2]/text()').extract_first().strip()
        item['category'] = response.xpath('//tr[1]/td[1]/a/text()').extract_first().strip()
        find_name_id = re.compile('\/(\d+)\.', re.S)
        name_id = re.findall(find_name_id, response.meta['url'])[0]
        item['name_id'] = name_id
        #print(item['name'],item['author'],item['serialstatus'],item['serialnum'],item['category'])
        self.count += 1
        print(self.count)
        return item


