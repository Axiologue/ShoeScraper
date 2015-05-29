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

# Spider for crawling Adidas website for shoes
class AsicsSpider(CrawlSpider):
    name = "asics"
    allowed_domains = ["asicsamerica.com"]
    start_urls = [
        "http://www.asicsamerica.com/Shop/Footwear/cat/Footwear/-/0-9999-featured",
    ]

    rules = (
        # Rule to go to the single product pages and run the parsing function
        # Excludes links that end in _W.html or _M.html, because they point to 
        # configuration pages that aren't scrapeable (and are mostly redundant anyway)
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@class,"image_link")]'),callback='singleProductParse'),

        )

    # Function to parse information from the product grid. Currently unused
    # OLD FROM NIKE SPIDER

    def ProductPageParse(self,response):
        products = response.css('div[id^="product-"]')[1:]
        for p in products:
            item = ProductItem()
            item['name'] = p.css('span.title').xpath('text()').extract()[0]
            item['brand'] = 'Asics'
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
        item['brand'] = 'Asics'
        item['name'] = response.css('h1').xpath('text()').extract()[0]


        #TRYING AND FAILING TO DELETE UNICODE CHARACTERS
        #item['name'] = name.encode('utf-8')

        # item['name'] = receivedbytes.decode("utf-8")
        # outbytes = item['name'].encode("utf-8")

        # item['name'].encode(encoding='UTF-8',errors='strict')

        # item['name'] = item[u'name']

        # item['name'] = item['name'].replace("charcters for trademark were here","")
        # item['name'] = item['name'].replace("characters for registered symbol were here","")
        desc = response.css('h4.product_type').xpath('text()').extract()[0].strip()
        if " Shoe" in desc:
                desc, _ = desc.split(" Shoe")
        try:
            item['division'], item['category'] = desc.split(" ",1)
            item['division'] = item['division'].replace("ens","en")
            item['category'] = item['category'].replace("footwear","")
        except ValueError:
            item['division'] = desc.replace("\'s","").replace("\'","")
            item['category'] = 'None'
        item['price'] = response.css('li.price').xpath('text()').extract()[0].strip()
        item['image_link'] = response.css('meta[property = "og:image"]::attr(content)').extract()[0]
        return item
