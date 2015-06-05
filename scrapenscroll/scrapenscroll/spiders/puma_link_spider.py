import scrapy

import json


from scrapenscroll.items import LinkItem


## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Puma website for shoes
class PumaLinkSpider(scrapy.Spider):
    name = "pumaLinks"
    allowed_domains = ["puma.com"]
    start_urls = [
        "http://us.puma.com/en_US/men/shoes",
        "http://us.puma.com/en_US/women/shoes",
        "http://us.puma.com/en_US/kids/boys/shoes",
        "http://us.puma.com/en_US/kids/girls/shoes",
    ]
    

    # Function to parse information from a single product page
    def parse(self,response):
        # Get All Script tags
        scripts = response.css('script').xpath('text()').extract()

        # Find tag that has 'pageData'
        data = filter(lambda k: 'pageData' in k,scripts)[0]

        # slice out 'pageData' variable content
        # So we can turn it into a python dict using json.loads
        js = data[data.index('{'):data.index(';')]

        # convert to python dictionary
        js = json.loads(js) 

        items = js['items']

        for item in items:
            name = item['productName'].replace(' ','-').replace("'",'')
            productID = item['productID']

            url = "http://us.puma.com/en_US/pd/" + name + '/' + productID + '.html'

            link = LinkItem();
            link['url'] = url

            yield link