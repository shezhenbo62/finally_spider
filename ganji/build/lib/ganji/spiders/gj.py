# -*- coding: utf-8 -*-
import scrapy
import json
from urllib import parse
from ganji.items import GanjiItem
import time
from copy import deepcopy
# import logging
#
# logger = logging.getLogger('ganji')


class GjSpider(scrapy.Spider):
    name = 'gj'
    allowed_domains = ['wh.ganji.com/fang1']
    start_urls = ['http://wh.ganji.com/fang1/']

    def parse(self, response):
        div_list = response.xpath("//div[@class='f-list js-tips-list']/div")
        for div in div_list:
            item = GanjiItem()
            # item = {}
            item['title'] = div.xpath(".//dd[@class='dd-item title']/a/text()").extract_first()
            b_href = div.xpath(".//dd[@class='dd-item title']/a/@href").extract_first()
            if b_href.startswith('http'):
                item['b_href'] = b_href
            else:
                item['b_href'] = 'http://wh.ganji.com' + b_href
            item['rent_type'] = div.xpath("./dl/dd[2]/span[1]/text()").extract_first()
            item['room_type'] = div.xpath("./dl/dd[2]/span[3]/text()").extract_first()
            item['room_size'] = div.xpath("./dl/dd[2]/span[5]/text()").extract_first()
            item['Orientation'] = div.xpath("./dl/dd[2]/span[7]/text()").extract_first()  # 朝向
            data = div.xpath("./dl/dd[3]/span")
            item['address'] = data.xpath("string(.)").extract_first().replace(' ','').replace('\n','')
            item['price'] = div.xpath("./dl/dd[last()]/div[1]//text()").extract_first()
            item['pub_time'] = div.xpath("./dl/dd[last()]/div[2]/text()").extract_first()
            time.sleep(1)
            yield scrapy.Request(item['b_href'],
                                 callback=self.get_detail_info,
                                 dont_filter=True,
                                 meta={'item':deepcopy(item)})

        #下一页
        next_url = 'http://wh.ganji.com' + response.xpath("//a[@class='next']/@href").extract_first()
        if next_url:
            yield scrapy.Request(next_url,
                                 callback=self.parse,
                                 dont_filter=True,
                                 meta={'item':item})

    def get_detail_info(self,response):
        # '''添加日志信息'''
        # print('print', response.url)
        # logger.info(response.url)
        # logger.debug(response.url)
        # logger.warning(response.url)
        # logger.error(response.url)

        item = response.meta['item']
        div_list = response.xpath("//div[@class='card-info f-fr']")
        for div in div_list:
            item['seller'] = div.xpath(".//div[@class='user-info-top']/p/text()").extract_first().strip()
            item['complate'] = div.xpath(".//div[@class='user-info-top']/div/span/text()").extract_first()
            user_id = div.xpath(".//div[@class='user-info-top']/p/input[1]/@value").extract_first()
            data_phone = div.xpath(".//div[@id='full_phone_show']/@data-phone").extract_first()
            if data_phone is not None:
                data_phone = parse.quote_plus(data_phone)
                s_href = "http://wh.ganji.com/ajax.php?dir=house&module=secret_phone&user_id="+user_id+"&phone="+data_phone+"&isPrivate=1"
                yield scrapy.Request(s_href,
                                    callback=self.get_phone,
                                    dont_filter=True,
                                    meta={'item':item})
            else:
                item['phone'] = None
                # print(item)
                yield item

    def get_phone(self,response):
        item = response.meta['item']
        item['phone'] = json.loads(response.body)['secret_phone']
        yield item
