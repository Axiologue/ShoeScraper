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
class FilaSpider(CrawlSpider):
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

    divisions = {
        "http://www.fila.com/kids-girls/shoes" : "Girls",
        "http://www.fila.com/kids-boys/shoes" : "Boys",
        "http://www.fila.com/energized-5" : "Women",
        "http://www.fila.com/womens-shoes/memory" : "Women",
        "http://www.fila.com/womens-shoes/casual" : "Women",
        "http://www.fila.com/womens-shoes/running" : "Women",
        "http://www.fila.com/womens-shoes/tennis" : "Women",
        "http://www.fila.com/energized-4" : "Men",
        "http://www.fila.com/mens-shoes/basketball" : "Men",
        "http://www.fila.com/mens-shoes/casual" : "Men",
        "http://www.fila.com/mens-shoes/running" : "Men",
        "http://www.fila.com/mens-shoes/tennis" : "Men",
        "http://www.fila.com/mens-shoes/memory" : "Men"
    }

    categories = {
        "http://www.fila.com/kids-girls/shoes" : "Kids Shoes",
        "http://www.fila.com/kids-boys/shoes" : "Kids Shoes",
        "http://www.fila.com/energized-5" : "Energized",
        "http://www.fila.com/womens-shoes/memory" : "Memory",
        "http://www.fila.com/womens-shoes/casual" : "Casual",
        "http://www.fila.com/womens-shoes/running" : "Running",
        "http://www.fila.com/womens-shoes/tennis" : "Tennis",
        "http://www.fila.com/energized-4" : "Energized",
        "http://www.fila.com/mens-shoes/basketball" : "Basketball",
        "http://www.fila.com/mens-shoes/casual" : "Casual",
        "http://www.fila.com/mens-shoes/running" : "Running",
        "http://www.fila.com/mens-shoes/tennis" : "Tennis",
        "http://www.fila.com/mens-shoes/memory" : "Memory"
    }


    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(restrict_xpaths='//a[@class="name-link"]'),
                #deny=('_[WM]\.html',)),
                callback='singleProductParse'),
            # Rule to follow arrow to next product grid
            #Rule(LinkExtractor(restrict_xpaths='//li[@class="pagging-arrow right-arrow"]'),
                #follow=True),
        )


    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()
        item['brand'] = 'Fila'
        name = response.css('.product-name ').xpath('text()').extract()[0]
        item['name'] = name.replace("women's ", "").replace("men's ", "").replace("kid's ", "")
        start_div = response.request.headers.get('Referer',None)
        item['division'] = self.divisions[start_div]
        start_cat = response.request.headers.get('Referer',None)
        item['category'] = self.categories[start_cat]


        price = response.css('.product-price')
        if (response.css('.product-price div')):
            price = response.css('.product-price div').xpath('text()').extract()[0].strip()
            price = price.split()[0].replace("$","")
        elif (response.css('.product-price .price-standard')):
            price = response.css('.price-standard').xpath('text()').extract()[0].strip()
            price = price.replace("$","")
        else:
            price = response.css('.product-price').xpath('text()').extract()[0].strip()
            price = price.replace("$", "")
        item['price'] = price

        item['image_link'] =  response.css('meta[name="sailthru.image.full"]').xpath('@content').extract()[0]
        return item
        
