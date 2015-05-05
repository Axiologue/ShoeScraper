import scrapy
import json

from scrapenscroll.items import ProductItem

class NikeSpider(scrapy.Spider):
    name = "nike"
    allowed_domains = ["nike.com"]

    url_list = ['http://store.nike.com/html-services/gridwallData?country=US&lang_locale=en_US&gridwallPath=shoes/brk&pn={0}'.format(i) for i in range(1,19)]
    #url_list = ['http://store.nike.com/html-services/gridwallData?country=US&lang_locale=en_US&gridwallPath=shoes/brk&pn=1']
    start_urls = url_list

    def parse(self,response):
        converted = json.loads(response.body)
        for product in converted['sections'][0]['products']:
            item = ProductItem()
            item['name'] = product['title']
            item['brand'] = 'Nike'
            desc = product['subtitle']
            if " Shoe" in desc:
                desc, _ = desc.split(" Shoe")
            try:
                item['division'], item['category'] = desc.split(" ",1)
                item['division'] = item['division'].replace("\'s","").replace("\'","")
            except ValueError:
                item['division'] = desc.replace("\'s","").replace("\'","")
                item['category'] = 'None'
            item['price'] = product['localPrice']
            item['image_link'] = product['spriteSheet']
            yield item