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
class EthleticSpider(CrawlSpider):
    name = "ethletic"
    download_delay = 0.25
    allowed_domains = ["ethletic.com"]
    start_urls = [
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-hi-cut/",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-lo-cut/",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-hi-cut/",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-lo-cut/",
        "http://shop.ethletic.com/en/skater/",
        "http://shop.ethletic.com/en/fair-deck/",
        "http://shop.ethletic.com/en/fair-loafer/",
        "http://shop.ethletic.com/en/ladies/",
        "http://shop.ethletic.com/en/fair-flip/",
        "http://shop.ethletic.com/en/fair-fighter/"
    ]

    divisions = {
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-hi-cut/" : "None",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-lo-cut/" : "None",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-hi-cut/" : "None",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-lo-cut/": "None",
        "http://shop.ethletic.com/en/skater/" : "None",
        "http://shop.ethletic.com/en/fair-deck/" : "None",
        "http://shop.ethletic.com/en/fair-loafer/" : "None",
        "http://shop.ethletic.com/en/ladies/" : "Women",
        "http://shop.ethletic.com/en/fair-flip/" : "None",
        "http://shop.ethletic.com/en/fair-fighter/" : "None"
    }


    categories = {
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-hi-cut/" : "Trainer White Cap High Cut",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-white-cap/fair-trainer-white-cap-lo-cut/" : "Trainer White Cap Low Cut",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-hi-cut/" : "Trainer Black Cap High Cut",
        "http://shop.ethletic.com/en/fair-trainer/fair-trainer-black-cap/fair-trainer-black-cap-lo-cut/": "Trainer Black Cap Low Cut",
        "http://shop.ethletic.com/en/skater/" : "Skater",
        "http://shop.ethletic.com/en/fair-deck/" : "Deck",
        "http://shop.ethletic.com/en/fair-loafer/" : "Loafer",
        "http://shop.ethletic.com/en/ladies/" : "Dancer",
        "http://shop.ethletic.com/en/fair-flip/" : "Flip",
        "http://shop.ethletic.com/en/fair-fighter/" : "Fighter"
    }


    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(restrict_xpaths='//div[contains(@class,"info strict")]'),
                #deny=('_[WM]\.html',)),
                callback='singleProductParse'),
            # Rule to follow arrow to next product grid
            #Rule(LinkExtractor(restrict_xpaths='//li[@class="pagging-arrow right-arrow"]'),
                #follow=True),
        )


    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()
        item['brand'] = 'Ethetic'
        name = response.css('title').xpath('text()').extract()[0]
        item['name'] = name.replace("- Ethletic-Sneaker","").replace("Ethletic","")
        start_div = response.request.headers.get('Referer',None)
        item['division'] = self.divisions[start_div]
        start_cat = response.request.headers.get('Referer',None)
        item['category'] = self.categories[start_cat]


        price = response.css('.price').xpath('text()').extract()[0]
        price = price.encode('ascii', 'ignore').strip()
        # product shows up twice, when the price is 0,00 ignore it
        if (price == "0,00"):
            return None
        item['price'] = price.replace(",", ".")

        item['image_link'] = response.css('.zoom img').xpath('@src').extract()[0]
        return item
        
