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
class NorthFaceSpider(CrawlSpider):
    name = "northface"
    allowed_domains = ["https://www.thenorthface.com/shop/shoes"]
    start_urls = [
        "https://www.thenorthface.com/shop/shoes-mens-winter-boots"
        "https://www.thenorthface.com/shop/shoes-mens-hiking",
        "https://www.thenorthface.com/shop/shoes-mens-running-training",
        "http://www.mizunousa.com/Running/Youth"
    ]

    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(restrict_xpaths='//a[@class="title"]'),
                #deny=('_[WM]\.html',)),
                callback='singleProductParse'),
            # Rule to follow arrow to next product grid
            #Rule(LinkExtractor(restrict_xpaths='//li[@class="pagging-arrow right-arrow"]'),
                #follow=True),
        )


    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()
        item['brand'] = 'Mizuno'
        item['category'] = 'Running Shoes'
        desc = response.css('title').xpath('text()').extract()[0]
        desc = desc.replace("| Mizuno USA","")
        item['division'], item['name'] = desc.split(" ",1)
        item['division'] = item['division'].replace("'s","")
        if item['division'] != "Men" and item['division'] != "Women" and item['division'] != "Unisex":
            item['division'] = "Youth"
            item['name'] = desc
        item['price'] = response.css('.price').xpath('text()').extract()[0].strip().replace("USD$","")
        item['image_link'] =  response.css('.product-slide img::attr(src)').extract()[0]
        return item
