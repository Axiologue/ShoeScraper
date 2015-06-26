import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapenscroll.items import ProductItem


## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Reebok website for shoes
class ReebokSpider(CrawlSpider):
    name = "reebok"
    allowed_domains = ["reebok.com"]
    start_urls = [
        "http://www.reebok.com/us/shoes",
    ]

    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(restrict_xpaths='//a[contains(@class,"product-link")]',
                deny=('_[WM]\.html',)),
                callback='singleProductParse'),
            # Rule to follow arrow to next product grid
            Rule(LinkExtractor(restrict_xpaths='//li[@class="pagging-arrow right-arrow"]'),
                follow=True),
        )

    # Function to parse information from the product grid. Currently unused
    # old one, not using it.
    def productPageParse(self,response):
        products = response.css('div[id^="product-"]')[1:]
        for p in products:
            item = ProductItem()
            item['name'] = p.css('span.title').xpath('text()').extract()[0]
            item['brand'] = 'Reebok'
            desc = p.css('span.subtitle').xpath('text()').extract()[0]
            try:
                item['division'], item['category'] = desc.split(" ",1)
            except ValueError:
                item['category'] = desc
                item['division'] = 'None'
            item['price'] = p.css('span.salesprice').xpath('text()').extract()[0].strip()
            item['image_link'] = p.css('img.show::attr(data-stackmobileview)').extract()[0]
            yield item

    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()
        item['brand'] = 'Reebok'
        item['name'] = response.css('.title-32').xpath('text()').extract()[0]
        desc = response.css('.title-16').xpath('text()').extract()[0].strip()
        try:
            item['division'], item['category'] = desc.split(" ",1)
        except ValueError:
            item['category'] = desc
            item['division'] = 'None'
        item['price'] = response.css('span.sale-price').xpath('text()').extract()[0].strip()
        item['image_link'] =  response.css('li.pdp-image-carousel-active-item img::attr(data-image)').extract()[0]
        return item
