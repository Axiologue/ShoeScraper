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
    name = "fila"
    allowed_domains = ["fila.com"]
    start_urls = [
        "http://www.fila.com/kids-girls/shoes",
        "http://www.fila.com/kids-boys/shoes",
        "http://www.fila.com/energized-5",
        "http://www.fila.com/womens-shoes/memory",
        "http://www.fila.com/womens-shoes/casual",
        "http://www.fila.com/womens-shoes/running",
        "http://www.fila.com/womens-shoes/tennis",
        "http://www.fila.com/energized-4",
        "http://www.fila.com/mens-shoes/basketball",
        "http://www.fila.com/mens-shoes/casual",
        "http://www.fila.com/mens-shoes/running",
        "http://www.fila.com/mens-shoes/tennis",
        "http://www.fila.com/mens-shoes/memory"
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


    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()
        item['brand'] = 'Fila'
        desc = response.css('.product-name a').xpath('text()').extract()[0]
        try:
            item['division'], item['name'] = desc.split(" ",1)
        except ValueError:
            item['division'] = div.replace("'s","")
            item['name'] = desc
        sales = response.css('span.product-sales-price').xpath('text()').extract()[0].strip()
        #if sales is empty then grab product-standard-price
        item['price'] = response.css('span.sales-price', 'product-standard-price').xpath('text()').extract()[0].strip()
        item['image_link'] =  response.css('li.pdp-image-carousel-active-item img::attr(data-image)').extract()[0]
        return item
