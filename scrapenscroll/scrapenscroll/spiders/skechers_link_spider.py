
import scrapy
import json 


from scrapenscroll.items import LinkItem

# Spider for crawling Skechers website for shoes' links
class SkechersLinkSpider(scrapy.Spider):
    name = "skechersLinks"
    allowed_domains = ["skechers.com"]

    labels = [ {'label': 'men', 'max': 5},{'label': 'women', 'max': 6},
     {'label': 'boys', 'max': 2}, {'label': 'girls', 'max': 2}]

    links=[]

    for label in labels:
        for page in range (1,label['max']+1 ):
            links.append("http://www.skechers.com/api/{0}/styles/athletic-shoes?p={1}".format(label['label'], page)) 

    start_urls = links

    # Function to parse information from a single product page
    def parse(self,response):

        js = json.loads(response.body)

        for record in js['search-results']['records']['record']:
            record['@key']

            url = "http://www.skechers.com/style" + record['@key']
            link = LinkItem();
            link['url'] = url

            yield link 
