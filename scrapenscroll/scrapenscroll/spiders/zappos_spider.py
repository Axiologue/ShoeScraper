import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.utils.spider import iterate_spider_output

from scrapenscroll.items import ProductItem

import re

## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Zappos website for shoes
class ZapposSpider(CrawlSpider):
    name = "zappos"
    allowed_domains = ["zappos.com"]
    start_urls = [
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AsALUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6At8LUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AssLUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AtALUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AvIKUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AtULUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AsYLUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AqANUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Ao0KUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgEL4gIEAQoCBw.zso",
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6ArMLUgEL4gIEAQoCBw.zso",
        
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2eC1IBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw22ClIBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3AC1IBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3LC1IBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3QC1IBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3yClIBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3VC1IBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3NCVIBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3GC1IBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3mClIBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw39ClIBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3fCVIBAeICBAoBBwc.zso?",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2QC1IBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3vCVIBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2zC1IBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2lC1IBAeICBAoBBwc.zso",
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2bClIBAeICBAoBBwc.zso?",

        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgLUHOICBAECCgc.zso",
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgLUHOICBAECCgc.zso?",
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6AssLUgLUHOICBAECCgc.zso?",
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6AtULUgLUHOICBAECCgc.zso",
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgLUHOICBAECCgc.zso?",

        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgEa4gIEAQoCBw.zso",
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AssLUgEa4gIEAQoCBw.zso?",
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AtULUgEa4gIEAQoCBw.zso",
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AsYLUgEa4gIEAQoCBw.zso",

        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToC1QtSASTiAgMKAQc.zso",
        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToCmg1SASTiAgMKAQc.zso",
        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToCpQtSASTiAgMKAQc.zso",

        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKXGuICBAEKAgc.zso",
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6AssLUgKXGuICBAEKAgc.zso?",
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6AtULUgKXGuICBAEKAgc.zso",
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgKXGuICBAEKAgc.zso",

        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgFU4gIEAQoCBw.zso",
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6AsALUgFU4gIEAQoCBw.zso",
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6AqULUgFU4gIEAQoCBw.zso",
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgFU4gIEAQoCBw.zso",

        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCngtSArcD4gIDCgEH.zso?",
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCywtSArcD4gIDCgEH.zso?",
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToC1QtSArcD4gIDCgEH.zso?",
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCzQlSArcD4gIDCgEH.zso?",
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToC_QpSArcD4gIDCgEH.zso",

        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCngtSAqcE4gIDCgEH.zso",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCtgpSAqcE4gIDCgEH.zso?",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCywtSAqcE4gIDCgEH.zso",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC0AtSAqcE4gIDCgEH.zso?",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC5gpSAqcE4gIDCgEH.zso?",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC3wlSAqcE4gIDCgEH.zso?",
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCsRRSAqcE4gIDCgEH.zso?",


        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCngtSAWviAgMKAQc.zso",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCtgpSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCwAtSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCywtSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC8gpSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC1QtSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCxgtSAWviAgMKAQc.zso?",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC_QpSAWviAgMKAQc.zso",
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC3wlSAWviAgMKAQc.zso?",

        "http://www.zappos.com/newton-running-women-shoes~1#!/newton-running-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKtG-ICBAEKAgc.zso",

        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCngtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCtgpaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCwAtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCywtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC0AtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCsRRaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC5gpaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC3wlaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCkAtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC7wlaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCswtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/",

        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToCtgpaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/",
        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToCywtaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/",
        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToC_QpaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/",

        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCngtSAX3iAgMKAQc.zso",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCtgpSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCwAtSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCzwpSAX3iAgMKAQc.zso",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToC8gpSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToC7wlSAX3iAgMKAQc.zso",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCxgtSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCkAtSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCpQtSAX3iAgMKAQc.zso?",
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCswtSAX3iAgMKAQc.zso?",

        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCngtSAoAB4gIDCgEH.zso",
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCtgpSAoAB4gIDCgEH.zso?",
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCywtSAoAB4gIDCgEH.zso?",
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCzwpSAoAB4gIDCgEH.zso",
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToC1QtSAoAB4gIDCgEH.zso?",
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToC7wlSAoAB4gIDCgEH.zso?",

        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToCngtSAuME4gIDAQoH.zso",
        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToC_QpSAuME4gIDAQoH.zso?",
        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToCywtSAuME4gIDAQoH.zso",

        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCngtSAowB4gIDCgEH.zso",
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCxgtSAowB4gIDCgEH.zso?",
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCywtSAowB4gIDCgEH.zso?",
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToC1QtSAowB4gIDCgEH.zso?",
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCtgpSAowB4gIDCgEH.zso",

        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKVAeICBAoBAgc.zso?",
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgKVAeICBAoBAgc.zso?",
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6AvIKUgKVAeICBAoBAgc.zso?",
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6AtULUgKVAeICBAoBAgc.zso",
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgKVAeICBAoBAgc.zso?",

        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToCngtSArwH4gIDAQoH.zso",
        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToC1QtSArwH4gIDAQoH.zso?",
        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToCtgpSArwH4gIDAQoH.zso?",

        "http://www.zappos.com/timberland-boots~e#!/timberland-boots/CK_XARCz1wE6Av0KUgKgAeICBAoBAgc.zso",
        "http://www.zappos.com/timberland-boots~e#!/timberland-boots/CK_XARCz1wE6AtULUgKgAeICBAoBAgc.zso?",

        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCngtSAtMS4gIDCgEH.zso",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCtgpSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCywtSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC5gpSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC_QpSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC3wlSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC7wlSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCswtSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCkAtSAtMS4gIDCgEH.zso?",
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCsRRSAtMS4gIDCgEH.zso?",
    ]

    meta = {
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgEL4gIEAQoCBw.zso": ['ASICS','Running'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgEL4gIEAQoCBw.zso": ['ASICS','Crosstraining'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AsALUgEL4gIEAQoCBw.zso": ['ASICS','Tennis'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6At8LUgEL4gIEAQoCBw.zso": ['ASICS','Wrestling'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AssLUgEL4gIEAQoCBw.zso": ['ASICS','Trail Running'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AtALUgEL4gIEAQoCBw.zso": ['ASICS','Volleyball'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AvIKUgEL4gIEAQoCBw.zso": ['ASICS','Golf'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AtULUgEL4gIEAQoCBw.zso": ['ASICS','Walking'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AsYLUgEL4gIEAQoCBw.zso": ['ASICS','Track and Field'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6AqANUgEL4gIEAQoCBw.zso": ['ASICS','Triathalon'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Ao0KUgEL4gIEAQoCBw.zso": ['ASICS','Cheerleading'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgEL4gIEAQoCBw.zso": ['ASICS','Hiking'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgEL4gIEAQoCBw.zso": ['ASICS','Indoor Court'],
        "http://www.zappos.com/asics-shoes~V#!/asics-sneakers-athletic-shoes/CK_XARC81wE6ArMLUgEL4gIEAQoCBw.zso": ['ASICS','Soccer'],
        
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2eC1IBAeICBAoBBwc.zso": ['Adidas','Running'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw22ClIBAeICBAoBBwc.zso?": ['Adidas','Crosstraining'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3AC1IBAeICBAoBBwc.zso?": ['Adidas','Tennis'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3LC1IBAeICBAoBBwc.zso?": ['Adidas','Trail Running'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3QC1IBAeICBAoBBwc.zso?": ['Adidas','Volleyball'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3yClIBAeICBAoBBwc.zso": ['Adidas','Golf'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3VC1IBAeICBAoBBwc.zso?": ['Adidas','Walking'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3NCVIBAeICBAoBBwc.zso": ['Adidas','Amphibious'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3GC1IBAeICBAoBBwc.zso?": ['Adidas','Track and Field'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3mClIBAeICBAoBBwc.zso": ['Adidas','Football'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw39ClIBAeICBAoBBwc.zso?": ['Adidas','Hiking'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3fCVIBAeICBAoBBwc.zso?": ['Adidas','Baseball and Softball'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2QC1IBAeICBAoBBwc.zso": ['Adidas','Indoor Court'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw3vCVIBAeICBAoBBwc.zso": ['Adidas','Basketball'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2zC1IBAeICBAoBBwc.zso": ['Adidas','Soccer'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2lC1IBAeICBAoBBwc.zso": ['Adidas','Skate'],
        "http://www.zappos.com/adidas-shoes~1Z#!/adidas-shoes/CK_XAToEnw2bClIBAeICBAoBBwc.zso?": ['Adidas','Climbing'],

        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgLUHOICBAECCgc.zso": ['Altra','Running'],
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgLUHOICBAECCgc.zso?": ['Altra','Crosstraining'],
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6AssLUgLUHOICBAECCgc.zso?": ['Altra','Trail Running'],
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6AtULUgLUHOICBAECCgc.zso": ['Altra','Walking'],
        "http://www.zappos.com/altra-zero-drop-footwear-women-sneakers-athletic-shoes~1#!/altra-zero-drop-footwear-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgLUHOICBAECCgc.zso?": ['Altra','Track and Field'],

        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgEa4gIEAQoCBw.zso": ['Brooks','Running'],
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AssLUgEa4gIEAQoCBw.zso?": ['Brooks','Trail Running'],
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AtULUgEa4gIEAQoCBw.zso": ['Brooks','Walking'],
        "http://www.zappos.com/brooks-shoes~3#!/brooks-sneakers-athletic-shoes/CK_XARC81wE6AsYLUgEa4gIEAQoCBw.zso": ['Brooks','Track and Field'],

        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToC1QtSASTiAgMKAQc.zso": ['Converse','Walking'],
        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToCmg1SASTiAgMKAQc.zso": ['Converse','Casual'],
        "http://www.zappos.com/converse-women~2#!/converse-shoes/CK_XAToCpQtSASTiAgMKAQc.zso": ['Converse','Skate'],

        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKXGuICBAEKAgc.zso": ['HokaOneOne','Running'],
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6AssLUgKXGuICBAEKAgc.zso?": ['HokaOneOne','Trail Running'],
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6AtULUgKXGuICBAEKAgc.zso": ['HokaOneOne','Walking'],
        "http://www.zappos.com/hoka-one-one-women-shoes~1#!/hoka-one-one-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgKXGuICBAEKAgc.zso": ['HokaOneOne','Hiking'],

        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgFU4gIEAQoCBw.zso": ['K-Swiss','Running'],
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6AsALUgFU4gIEAQoCBw.zso": ['K-Swiss','Tennis'],
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6AqULUgFU4gIEAQoCBw.zso": ['K-Swiss','Skate'],
        "http://www.zappos.com/k-swiss-womens-shoes~5#!/k-swiss-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgFU4gIEAQoCBw.zso": ['K-Swiss','Crosstraining'],

        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCngtSArcD4gIDCgEH.zso?": ['Merrell','Running'],
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCywtSArcD4gIDCgEH.zso?": ['Merrell','Trail Running'],
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToC1QtSArcD4gIDCgEH.zso?": ['Merrell','Walking'],
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToCzQlSArcD4gIDCgEH.zso?": ['Merrell','Amphibious'],
        "http://www.zappos.com/merrell-shoes~g#!/merrell-shoes/CK_XAToC_QpSArcD4gIDCgEH.zso": ['Merrell','Hiking'],

        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCngtSAqcE4gIDCgEH.zso": ['Mizuno','Running'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCtgpSAqcE4gIDCgEH.zso?": ['Mizuno','Crosstraining'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCywtSAqcE4gIDCgEH.zso": ['Mizuno','Trail Running'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC0AtSAqcE4gIDCgEH.zso?": ['Mizuno','Volleyball'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC5gpSAqcE4gIDCgEH.zso?": ['Mizuno','Football'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToC3wlSAqcE4gIDCgEH.zso?": ['Mizuno','Baseball and Softball'],
        "http://www.zappos.com/mizuno-womens~3#!/mizuno-shoes/CK_XAToCsRRSAqcE4gIDCgEH.zso?": ['Mizuno','Lacrosse'],


        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCngtSAWviAgMKAQc.zso": ['New Balance','Running'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCtgpSAWviAgMKAQc.zso?": ['New Balance','Crosstraining'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCwAtSAWviAgMKAQc.zso?": ['New Balance','Tennis'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCywtSAWviAgMKAQc.zso?": ['New Balance','Trail Running'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC8gpSAWviAgMKAQc.zso?": ['New Balance','Golf'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC1QtSAWviAgMKAQc.zso?": ['New Balance','Walking'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToCxgtSAWviAgMKAQc.zso?": ['New Balance','Track and Field'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC_QpSAWviAgMKAQc.zso": ['New Balance','Hiking'],
        "http://www.zappos.com/new-balance-shoes~1n#!/new-balance-shoes/CK_XAToC3wlSAWviAgMKAQc.zso?": ['New Balance','Baseball and Softball'],

        "http://www.zappos.com/newton-running-women-shoes~1#!/newton-running-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKtG-ICBAEKAgc.zso": ['Newton','Running'],

        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCngtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Running'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCtgpaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Crosstraining'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCwAtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Tennis'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCywtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Trail Running'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC0AtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Volleyball'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCsRRaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Lacrosse'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC5gpaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Football'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC3wlaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Baseball and Softball'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCkAtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Indoor Court'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToC7wlaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Basketball'],
        "http://www.zappos.com/nike-mens-shoes~4u?s=goliveRecentSalesStyle/desc/#!/nike-shoes/CK_XAToCswtaAW_iAgMLAQc.zso?s=goliveRecentSalesStyle/desc/": ['Nike','Soccer'],

        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToCtgpaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/": ['North Face','Crosstraining'],
        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToCywtaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/": ['North Face','Trail Running'],
        "http://www.zappos.com/shoes~7J#!/shoes/CK_XAToC_QpaBOIE4QniAgMBCwc.zso?s=isNew/desc/recentSalesStyle/desc/goLiveDate/desc/": ['North Face','Hiking'],

        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCngtSAX3iAgMKAQc.zso": ['Puma','Running'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCtgpSAX3iAgMKAQc.zso?": ['Puma','Crosstraining'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCwAtSAX3iAgMKAQc.zso?": ['Puma','Tennis'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCzwpSAX3iAgMKAQc.zso": ['Puma','Dance'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToC8gpSAX3iAgMKAQc.zso?": ['Puma','Golf'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToC7wlSAX3iAgMKAQc.zso": ['Puma','Basketball'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCxgtSAX3iAgMKAQc.zso?": ['Puma','Track and Field'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCkAtSAX3iAgMKAQc.zso?": ['Puma','Indoor Court'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCpQtSAX3iAgMKAQc.zso?": ['Puma','Skate'],
        "http://www.zappos.com/puma-shoes~2j#!/puma-shoes/CK_XAToCswtSAX3iAgMKAQc.zso?": ['Puma','Soccer'],

        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCngtSAoAB4gIDCgEH.zso": ['Reebok','Running'],
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCtgpSAoAB4gIDCgEH.zso?": ['Reebok','Crosstraining'],
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCywtSAoAB4gIDCgEH.zso?": ['Reebok','Trail Running'],
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToCzwpSAoAB4gIDCgEH.zso": ['Reebok','Dance'],
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToC1QtSAoAB4gIDCgEH.zso?": ['Reebok','Walking'],
        "http://www.zappos.com/reebok-mens~3#!/reebok-shoes/CK_XAToC7wlSAoAB4gIDCgEH.zso?": ['Reebok','Basketball'],

        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToCngtSAuME4gIDAQoH.zso": ['Salomon','Running'],
        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToC_QpSAuME4gIDAQoH.zso?": ['Salomon','Hiking'],
        "http://www.zappos.com/salomon-womens-shoes~b#!/salomon-shoes/CK_XAToCywtSAuME4gIDAQoH.zso": ['Salomon','Trail Running'],

        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCngtSAowB4gIDCgEH.zso": ['Saucony','Running'],
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCxgtSAowB4gIDCgEH.zso?": ['Saucony','Track and Field'],
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCywtSAowB4gIDCgEH.zso?": ['Saucony','Trail Running'],
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToC1QtSAowB4gIDCgEH.zso?": ['Saucony','Walking'],
        "http://www.zappos.com/saucony-men~2#!/saucony-shoes/CK_XAToCtgpSAowB4gIDCgEH.zso": ['Saucony','Crosstraining'],

        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6Ap4LUgKVAeICBAoBAgc.zso?": ['Skechers','Running'],
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6Av0KUgKVAeICBAoBAgc.zso?": ['Skechers','Hiking'],
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6AvIKUgKVAeICBAoBAgc.zso?": ['Skechers','Golf'],
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6AtULUgKVAeICBAoBAgc.zso": ['Skechers','Walking'],
        "http://www.zappos.com/skechers-men~2#!/skechers-sneakers-athletic-shoes/CK_XARC81wE6ArYKUgKVAeICBAoBAgc.zso?": ['Skechers','Crosstraining'],

        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToCngtSArwH4gIDAQoH.zso": ['Spira','Running'],
        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToC1QtSArwH4gIDAQoH.zso?": ['Spira','Walking'],
        "http://www.zappos.com/spira-womens-shoes~3#!/spira-shoes/CK_XAToCtgpSArwH4gIDAQoH.zso?": ['Spira','Crosstraining'],

        "http://www.zappos.com/timberland-boots~e#!/timberland-boots/CK_XARCz1wE6Av0KUgKgAeICBAoBAgc.zso": ['Spira','Hiking'],
        "http://www.zappos.com/timberland-boots~e#!/timberland-boots/CK_XARCz1wE6AtULUgKgAeICBAoBAgc.zso?": ['Spira','Walking'],

        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCngtSAtMS4gIDCgEH.zso": ['Under Armour','Running'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCtgpSAtMS4gIDCgEH.zso?": ['Under Armour','Crosstraining'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCywtSAtMS4gIDCgEH.zso?": ['Under Armour','Trail Running'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC5gpSAtMS4gIDCgEH.zso?": ['Under Armour','Football'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC_QpSAtMS4gIDCgEH.zso?": ['Under Armour','Hiking'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC3wlSAtMS4gIDCgEH.zso?": ['Under Armour','Baseball and Softball'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToC7wlSAtMS4gIDCgEH.zso?": ['Under Armour','Basketball'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCswtSAtMS4gIDCgEH.zso?": ['Under Armour','Soccer'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCkAtSAtMS4gIDCgEH.zso?": ['Under Armour','Indoor Court'],
        "http://www.zappos.com/under-armour-shoes~5#!/under-armour-shoes/CK_XAToCsRRSAtMS4gIDCgEH.zso?": ['Under Armour','Lacrosse'],
    }


    rules = (
            # Rule to go to the single product pages and run the parsing function
            # Excludes links that end in _W.html or _M.html, because they point to 
            # configuration pages that aren't scrapeable (and are mostly redundant anyway)
            Rule(LinkExtractor(restrict_xpaths='//a[contains(@class,"product")]'),
                #deny=('_[WM]\.html',)),
                callback='singleProductParse'),
            # Rule to follow arrow to next product grid
            Rule(LinkExtractor(restrict_xpaths="//div[contains(@class,'pagination')]/a[last()]"),
                follow=True),
        )


    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                if isinstance(request_or_item, Request):
                    request_or_item.meta['start_url'] = response.meta['start_url']
                yield request_or_item

    def make_requests_from_url(self, url):
        """A method that receives a URL and returns a Request object (or a list of Request objects) to scrape. 
        This method is used to construct the initial requests in the start_requests() method, 
        and is typically used to convert urls to requests.
        """
        return Request(url, dont_filter=True, meta = {'start_url': url})

    # Function to parse information from a single product page
    def singleProductParse(self,response):
        item = ProductItem()

        # Get meta data from link
        res = response.request.meta['start_url'] 
        start_url = res.replace('?_escaped_fragment_=%2F','#!/').replace('%2F','/')
        item['brand'] = self.meta[start_url][0]
        item['category'] = self.meta[start_url][1]

        scripts = response.css('script').xpath('text()').extract()
        data = filter(lambda k: 'productGender' in k,scripts)[0]
        gender = re.search('var productGender = (.*?);', data).group(1)

        item['division'] = gender.replace('"','')

        name = response.css('.ProductName').xpath('text()').extract()[0]
        item['name'] = name


        price = response.css('.nowPrice').xpath('text()').extract()[0]
        item['price'] = price.replace("$", "")

        item['image_link'] = response.css('#spotlightLowResImage').xpath('@src').extract()[0]
        return item
        
