import scrapy
from scrapenscroll.items import ProductItem

class AdidasSpider(scrapy.Spider):
    name = "adidas"
    allowed_domains = ["adidas.com"]
    start_urls = [
        "http://www.adidas.com/us/shoes",
    ]

    def parse(self,response):
        products = response.css('div[id^="product-"]')[1:]
        for p in products:
            item = ProductItem()
            item['name'] = p.css('span.title').xpath('text()').extract()[0]
            item['brand'] = 'Adidas'
            desc = p.css('span.subtitle').xpath('text()').extract()[0]
            item['division'], item['category'] = desc.split(" ",1)
            item['price'] = p.css('span.salesprice').xpath('text()').extract()[0].strip()
            item['image_link'] = p.css('img.show::attr(data-stackmobileview)').extract()[0]
            yield item