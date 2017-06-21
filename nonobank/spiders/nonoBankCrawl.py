# -*- coding: utf-8 -*-
import scrapy
from nonobank.items import NonobankItem
from scrapy.selector import Selector
from scrapy.http.request import Request


class NonobankcrawlSpider(scrapy.Spider):
    name = "nonoBankCrawl"
    allowed_domains = ["nonobank.com"]
    # 分析借款用户
    start_urls = ['https://www.nonobank.com/Lend/View/' + str(i) for i in range(1, 2500000)]

    def start_requests(self):
        cookie = {
                  'is_checked_13237389':'true',
                  'UM_distinctid':'15cbea320fd552-01e5f6e51477f2-5393662-1fa400-15cbea320febc5',
                  'PHPSESSID':'qgrn7lkm42h8t7qchu3f6ds031',
                  '_fmdata':'8114C4E9E706965BEAA580E053FDA9ADBBCE606FC4DD189B3FB16A4D6AC7961344'
                  			'A59014073AAB659430E988FB8874E04E203F9E618C7745',
                  'jwt':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTMyMzczODksImlhdCI6MTQ5Nz'
                  		'k1NTc1OSwiZXhwIjoxNDk3OTU3NTU5fQ.6qz2OC6hwFIkrROAXU_Eh_42Uldjxyz0-uHS1d1BmMI',
                  'Hm_lvt_9507cba2915f8791df56ad059db2ffb6':'1497846966,1497860754,1497879297,1497955716',
                  'Hm_lpvt_9507cba2915f8791df56ad059db2ffb6':'1497956139'                 

                  }
        for url in self.start_urls:
            yield Request(url, cookies=cookie)

    def parse(self, response):
        if len(response.text) < 100:
            return
        sel = Selector(response)
        item = NonobankItem()
        item['purpose'] = sel.xpath('//div[@class="lend_left_box wid_per100"][1]/div/dl/dt/text()').extract_first()
        item['description'] = sel.xpath('//div[@class="lend_left_box wid_per100"][1]/div/dl/dd/text()').extract_first().split(':')[-1]

        loan_sel = sel.xpath('//div[@class="lend_left_box wid_per100"][3]/div/dl')
        item['total_loan'] = loan_sel.xpath('//dd[1]/span/text()').extract_first().replace('￥', '')
        item['loan_num'] = loan_sel.xpath('//dd[2]/span/text()').extract_first().replace('次', '')
        item['normal_pay_off'] = loan_sel.xpath('//dd[3]/span/text()').extract_first().replace('次', '')
        item['overdue_pay_off'] = loan_sel.xpath('//dd[4]/span/text()').extract_first().replace('次', '')
        item['overdue'] = loan_sel.xpath('//dd[5]/span/text()').extract_first().replace('次', '')
        item['to_paid'] = loan_sel.xpath('//dd[6]/span/text()').extract_first().replace('￥', '')

        item['userId'] = response.url.split('/')[-1]
        item['role'] = sel.xpath('//div[@class="box_left"]/p/text()').extract_first()

        item['name'] = sel.xpath('//div[@class="box_right"]/div[1]/a/@title').extract_first()
        #--------------------
        # 个人背景和行为
        #--------------------
        keys = list()
        values = list()
        infos = sel.xpath('//div[@class="box_right"]/div/text()').extract()
        for info in infos:
            if '：' in info:
                keys.append(info.replace('\xa0', '').split('：')[0])
                values.append(info.split('：')[1])
            else:
                continue
        moreInfo = dict(zip(keys, values))
        item['gender'] = moreInfo['性别']
        item['age'] = moreInfo['年龄']
        if moreInfo['户籍']:
        	item['registration'] = moreInfo['户籍']
        # item['location'] = moreInfo['所在地']
        item['province'] = moreInfo['所在地'].split(' ')[0]
        item['city'] = moreInfo['所在地'].split(' ')[-1]
        if item['role'] == '学生':
            item['school_name'] = sel.xpath('//div[@class="borrowing_box tablestyle"]/table/tbody/tr/td[1]/text()').extract_first().split('：')[-1]
            item['major'] = sel.xpath('//div[@class="borrowing_box tablestyle"]/table/tbody/tr/td[2]/text()').extract_first().split('：')[-1]
            item['admission_time'] = sel.xpath('//div[@class="borrowing_box tablestyle"]/table/tbody/tr/td[3]/text()').extract_first().split('：')[-1]
            item['marriage'] = None
            item['education'] = None
        else:
            item['marriage'] = moreInfo['婚姻']
            item['education'] = moreInfo['学历']
            item['school_name'] = None
            item['major'] = None
            item['admission_time'] = None
        yield item
