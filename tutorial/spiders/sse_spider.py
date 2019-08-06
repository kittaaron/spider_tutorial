# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
import re
import json
import string
from scrapy import cmdline
import demjson


class SseSpider(scrapy.Spider):
    name = "sse"

    def start_requests(self):

        urls = [
            'http://www.sse.com.cn/js/common/stocks/new/600060.js?_=1540457989823',

            'http://query.sse.com.cn/security/stock/queryCompanyStatementNew.do? ' +
            'jsonCallBack=jsonpCallback83935&isPagination=true&productId=600060&' +
            'keyWord=&isNew=1&reportType2=DQBG&reportType=ALL&beginDate=2015-10-26&endDate=2018-10-25&' +
            'pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&' +
            'pageHelp.cacheSize=1&pageHelp.endPage=5&_=1540460872289'
        ]
        for url in urls:
            payload_header = {
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Host': 'query.sse.com.cn',
                # "Origin": 'http://www.szse.cn',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Cookie': 'zg_did=%7B%22did%22%3A%20%22166eb67c8b6a61-028ada82691d84-1e3b6654-fa000-166eb67c8b889c%22%7D; saveFpTip=true; _uab_collina=154443535878193473103319; UM_distinctid=16a9676d70544e-06a0e9e3a62c59-36697e04-fa000-16a9676d7064ff; QCCSESSID=o4rt068st16qe9dhkpdanpc667; acw_tc=6547699815641361014984248eee70155f680bbd3e10a270bee19fefb1; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1563171783; CNZZDATA1254842228=1168838228-1541543103-https%253A%252F%252Fwww.baidu.com%252F%7C1565055157; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201565057127089%2C%22updated%22%3A%201565057174346%2C%22info%22%3A%201565054188203%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%221d62bbf24fdd2b4a66b95cba1fa6e421%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1565057183',
                'Host': 'www.qichacha.com',
                'Pragma': 'no-cache',
                'Referer': 'https://www.qichacha.com/',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
            }
            yield scrapy.Request(url=url, headers=payload_header,
                                 callback=self.parse)

    def parse(self, response):
        content = response.body.decode('utf8')
        print(content)
        extract_contents = re.findall(".*_t.push\((.*)\);", content)
        self.log('extract_contents: %s' % extract_contents)
        for contentI in extract_contents:
            json_content = demjson.decode(contentI)
            self.log('json_content %s' % json_content)
            bulletin_file_url = json_content['bulletin_file_url']
            bulletin_title = json_content['bulletin_title']

            if bulletin_title.find("报告") >= 0:
                self.log('title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            else:
                self.log('其他文档 -- title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            '''
            if bulletin_file_url.find("_z.pdf") >= 0 or \
                    bulletin_file_url.find("_n.pdf") >= 0 or \
                    bulletin_file_url.find("_1.pdf") >= 0 or \
                    bulletin_file_url.find("_3.pdf") >= 0:
                self.log('title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            else:
                self.log('其他文档 -- title: %s bulletin_file_url %s' % (bulletin_title, bulletin_file_url))
            '''
        # content = Selector(response=response).xpath('//a[contains(@href, "pdf")]').extract()
        # content = Selector(response=response).xpath('//a[contains(@href, "_1.pdf")]').extract()


if __name__ == '__main__':
    cmdline.execute("scrapy crawl sse".split())
    #spider = SseSpider()
    #spider.start_requests()
