import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapenscroll.items import ProductItem

class AdidasSpider(CrawlSpider):
    name = "adidas"
    allowed_domains = ["adidas.com"]
    start_urls = [
        "http://www.adidas.com/us/shoes",
    ]

    rules = (
            
            Rule(LinkExtractor(restrict_xpaths='//li[@class="pagging-arrow right-arrow"]'),
                callback='productPageParse',follow=True),
        )

    def productPageParse(self,response):
        products = response.css('div[id^="product-"]')[1:]
        for p in products:
            item = ProductItem()
            item['name'] = p.css('span.title').xpath('text()').extract()[0]
            item['brand'] = 'Adidas'
            desc = p.css('span.subtitle').xpath('text()').extract()[0]
            try:
                item['division'], item['category'] = desc.split(" ",1)
            except ValueError:
                item['category'] = desc
                item['division'] = 'None'
            item['price'] = p.css('span.salesprice').xpath('text()').extract()[0].strip()
            item['image_link'] = p.css('img.show::attr(data-stackmobileview)').extract()[0]
            yield item