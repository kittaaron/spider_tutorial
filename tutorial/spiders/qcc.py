# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
import urllib


BASE_URL = 'https://www.qichacha.com/search?key='


## 企查查爬虫
class QccSpider(scrapy.Spider):
    name = 'qichacha'
    allowed_domains = ['qichacha.com']

    search_keys = ['钱咚咚']


    def start_requests(self):
        urls = []
        for key_i in self.search_keys:
            key_word = urllib.parse.quote(key_i)
            re = BASE_URL + key_word
            urls.append(BASE_URL + key_word)

            #re = url
            search_index = r'https://www.qichacha.com/search_index?key={}&ajaxflag=1&'.format(key_word, 1)
            print("search_index: " + search_index + ", refer: " + re)
            payload_header = {
                'Host': 'www.qichacha.com',
                'Connection': 'keep-alive',
                'Accept': r'text/html, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                'Referer': re,
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                #'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                #'Accept-Language': 'zh-CN,zh;q=0.9',
                #'Accept-Encoding': 'gzip, deflate, br',
                #'Host': 'www.qichacha.com',
                #'Pragma': 'no-cache',
                #'Referer': 'https://www.qichacha.com/',
                #'Connection': 'keep-alive',
                'Cookie': r'_umdata=2FB0BDB3C12E491D5D6DE5A378AB522025ADFE6C0ECC2CD53488EFDFA289AC40177333EAD28B6A1CCD43AD3E795C914CA8D2B994323BD8DAD217BD465CB2C20D',
                #'Upgrade-Insecure-Requests': "1",
                #'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            #url += "&ajaxflag=1&p=1&"
            yield scrapy.Request(url=search_index, headers=payload_header,
                                 callback=self.parse)

    def parse(self, response):
        url = response.url
        content = response.body.decode('utf8')
        hrefs = response.xpath('//tbody[@id="search-result"]/td/a/@href').getall()
        print(hrefs)

if __name__ == '__main__':
    cmdline.execute("scrapy crawl qichacha".split())