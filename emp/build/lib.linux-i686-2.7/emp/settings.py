# -*- coding: utf-8 -*-

# Scrapy settings for emp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'emp'

SPIDER_MODULES = ['emp.spiders']
NEWSPIDER_MODULE = 'emp.spiders'
AJAXCRAWL_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'emp (+http://www.yourdomain.com)'

# #
# DOWNLOADER_MIDDLEWARES = {
# 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
# 'emp.middlewares.ProxyMiddleware': 100,
# 'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
# 'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': None,
# }

# BOT_NAME = 'employee_details'
#
# SPIDER_MODULES = ['employee_details.spiders']
# NEWSPIDER_MODULE = 'employee_details.spiders'
#
# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# #USER_AGENT = 'emp (+http://www.yourdomain.com)'
#
#
# DOWNLOADER_MIDDLEWARES = {
# 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
# 'employee_details.middlewares.ProxyMiddleware': 110,
# }
# #
