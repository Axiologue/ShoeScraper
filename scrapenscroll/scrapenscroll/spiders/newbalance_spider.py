import scrapy
import json
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapenscroll.items import ProductItem

class NewbalanceSpider(CrawlSpider):
    name = "newbalance"
    allowed_domains = ["newbalance.com"]

    list_nums = [i*24 for i in range(0, 37)]
    url_list = ['http://www.newbalance.com/search?start={0}&q=shoes&sz=24&format=ajax'.format(i) for i in list_nums]
    #url_list = ['http://store.nike.com/html-services/gridwallData?country=US&lang_locale=en_US&gridwallPath=shoes/brk&pn=1']
    start_urls = url_list

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@class="product-image"]'),callback='ProductPageParse'),
        )

    def ProductPageParse(self,response):
        
        item = ProductItem()
        item['name'] = response.css('.product-name').xpath('text()').extract()[0].strip()
        item['brand'] = 'NewBalance'            
        desc = response.css('h2.label').xpath('text()').extract()[0]
        try:
           item['division'], item['category'] = desc.split(" ",1)
           item['division'] = item['division'].replace("\'s","").replace("\'","")
        except ValueError:
           item['division'] = desc.replace("\'s","").replace("\'","")
           item['category'] = 'None'

        #Find the scrip tag with the utag_data variable, turn to json to extract json info
        scripts = response.css('script').xpath('text()').extract()
        data = filter(lambda k: 'utag_data' in k,scripts)[0]
        var = data[data.index('{'):data.index('}')+1]

        item['price'] = json.loads(var)['product_unit_price'][0]
        item['image_link'] = response.css('meta[property = "og:image"]::attr(content)').extract()[0]
        badCat = ['Shoe Care', 'Casuals', 'Flip Flops', 'Slides', 'Casual Footwear', 'Boots', 'Dress Shoes', 'Aravon by New Balance', 'Sandals', 'Dunham by New Balance', 'Work Shoes', 'Grade School Sandals', 'Infant Sandals', 'Pre-School Sandals', 'Safety', 'null']
        if  item['category'] not in badCat:
            return item