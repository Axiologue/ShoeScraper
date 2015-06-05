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

# Spider for crawling Puma website for shoes
class PumaSpider(CrawlSpider):
    name = "puma"
    allowed_domains = ["puma.com"]
    start_urls = [
        "http://us.puma.com/en_US/men/shoes",
        "http://us.puma.com/en_US/women/shoes",
        "http://us.puma.com/en_US/kids/shoes"
    ]
    

    # Function to parse information from a single product page
    def parse(self,response):
        item = ProductItem()
        item['brand'] = 'Puma'
        # Get category and Division from breadcrumb at top of page
        cat = response.css('ol.breadcrumb li:nth-last-child(1) a').xpath('text()').extract()[0];
        div = response.css('ol.breadcrumb li:nth-child(3) a').xpath('text()').extract()[0];
        # Use category and division to remove unnecessary info from title
        title = response.css('ol.breadcrumb li:last-child span').xpath('text()').extract()[0];
        item['name'] = title.replace(cat,"").replace(div,"")
        # Strip out unnecessary info from category/division
        item['division'] = div.replace("'s","")
        item['category'] = cat.replace("Shoes","")
        # Get image link
        item['image_link'] = response.css('.product-primary-image a:first-child img::attr(src)').extract()[0];
        # Select the set of prices, and then take the last one
        item['price'] = response.css('.price-sales').xpath('text()').extract()[0];
        return item