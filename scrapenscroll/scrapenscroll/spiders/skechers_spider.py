import scrapy
import csv
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapenscroll.items import ProductItem


# Spider for crawling Skechers website for shoes
class SkechersSpider(scrapy.Spider):
    name = "skechers"
    allowed_domains = ["skechers.com"]

    #Turn links into list
    f = open('skechersLinks.csv')
    reader = csv.reader(f)
    skechers_links = list(reader)
    skechers_links = [x[0] for x in skechers_links]
    skechers_links = skechers_links[1:]
    #print(len(links))
    start_urls = skechers_links


    # Function to parse information from a single product page
    def parse(self,response):
        item = ProductItem()
        item['brand'] = 'Skechers'
        item['name'] = response.css('style').xpath('@name').extract()[0]
        gender = response.css('style').xpath('@gender').extract()[0]
        if gender == 'W':
            item['division'] = 'Women'
        if gender == 'M':
            item['division'] = 'Men'
        if gender == 'G':
            item['division'] = 'Girls'
        if gender == 'B':
            item['division'] = 'Boys'


        style = response.css('style').extract()[0]
        style.index('price')
        startIndex = style.index('price')
        endIndex = (startIndex + 7)
        price = style[endIndex:endIndex + 6]
        item['price'] = price.replace("\"", "").replace(" ","")

        item['category'] = response.css('default-category-title').xpath('text()').extract()


        image = response.css('media').extract()[0]
        image.index('image')
        startIndexImg = image.index('image')
        endIndexImg = (startIndexImg + 7)
        link = image[endIndexImg:endIndexImg + 14].replace("\"", "").replace(" ","")

        item['image_link'] = "http://cdn4.skechers-usa.com/img/productimages/xlarge/" + link

        return item
