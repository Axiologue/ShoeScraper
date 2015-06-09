# -*- coding: utf-8 -*-

# Scrapy settings for scrapenscroll project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapenscroll'

SPIDER_MODULES = ['scrapenscroll.spiders']
NEWSPIDER_MODULE = 'scrapenscroll.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapenscroll (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'scrapenscroll.pipelines.DuplicatesPipeline': 300,
    #'scrapenscroll.pipelines.DuplicateLinksPipeline': 300,
    'scrapenscroll.pipelines.CSVPipeline': 400,
}
