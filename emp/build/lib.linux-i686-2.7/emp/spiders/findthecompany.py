import scrapy
import re
import csv
import string
import json
import urllib
from lxml import html
from scrapy.http import Request
from ..import items
from pkg_resources import resource_stream

include_package_data = True


class Employee_details(scrapy.Spider):
    name = "findthecompany"
    domain = "http://www.findthecompany.com"
    # start_urls = ['http://www.findthecompany.com/']
    listing_url = "http://listings.findthecompany.com/?launch_filters="
    # start_urls = ["http://listings.findthecompany.com/?launch_filters=%5B%7B%22field%22%3A%22company_name%22%2C%22operator%22%3A%22LIKE%22%2C%22value%22%3A%22BALLARD%20INC%22%7D%5D"]
    download_delay = 10
    # cookies = {
    #   '__ats':'1459751332921',
    #   '__gads':'ID=4321ce826e937ed0:T=1459167302:S=ALNI_MYwdf23TXcXNFWD1Pzf_Ju8K8EGCg',
    #   '_ftbuptc':'lbd8hF2nwF2svatTXJidu3oS0aSGYmbe',
    #   '_ftbuptcs':'6oqAgbQdMxSLNtrVhFJFva8I97PW7l92',
    #   '_ga':'GA1.2.896844723.1459167251',
    #   '_gat':'1',
    #   '_gqpv':'2',
    #   '_test_cookie':'1',
    #   'bknx_fa':'1459745964123',
    #   'bknx_ss':'1459745964123',
    #   'ftb_ip_information':'atitude%3D37.80922789999999%26longitude%3D-85.4669025%26place%3DBardstown%252C%252BKY%252C%252BUnited%252BStates%26postCode%3D40004'
    # }

    # cookies = {
    #    '__gads':'ID=42dcec9c0f59d097:T=1460012175:S=ALNI_Mapvj1vmNa7NofyArwUwCxrjLsbKQ',
    #    '__ybotu':'impxju3yccc0lyc6zw',
    #    '__ybotv':'1460023374014',
    #    'ftb_ip_information':'latitude%3D37.80922789999999%26longitude%3D-85.4669025%26place%3DBardstown%252C%2BKY'
    #                         '%252C%2BUnited%2BStates%26countryCode%3DUS',
    #   '_ga':'GA1.2.1683973197.1460012157',
    #   '__ats':'1460366759589',
    #   '_ftbuptc':'ybWzg02L9JBRxngrvPOtM4zyujCKuDHT',
    #   '_ftbuptcs':'3R2vGvg4bUMqxEuacyVrrGHxyxFgdF76',
    #   'D_PID':'83606733-E95D-3A79-89BC-0894730FBB78',
    #   'D_IID':'EF5267B7-C7D0-3114-9F32-68C72BEC5B1B',
    #   'D_UID':'85070DE7-E0ED-3A70-B216-17BAFAE7CD27',
    #   'D_HID':'SHZZ3Mb2VxUalw7SNf4UfoPy1HtVlOsimfKrsuGbb8w',
    #
    # }

    # headers = {
      # 'Host': 'www.findthecompany.com',
      # 'Connection': 'keep-alive',
      # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      # 'User-Agent': 'Googlebot/2.1'
      # 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) '
      #               'Chrome/36.0.1985.143Safari/537.36'

      # 'Accept-Encoding': 'gzip,deflate,sdch',
      # 'Accept-Language': 'en-US,en;q=0.8',

    # }

    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,​*/*​;q=0.8',
      'Accept-Encoding': 'gzip, deflate, sdch',
      'Accept-Language': 'en-US,en;q=0.8,arq=0.6',
      'Connection': 'keep-alive',

      'Host': 'listings.findthecompany.com',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                    'Chromium/49.0.2623.87Chrome/49.0.2623.87 Safari/537.36'
    }

    cookies = {
       # 'D_SID': '182.75.158.122:F9Btotg0SQ2ZL+HfYAdl3pc99nxsNBrXqAw9oqJlERI',
       'D_PID': '2FD039D9-3690-3ECD-8EEC-6FB31020F488',
       'D_IID': '3E7B8459-1886-31CF-88AB-477FA5D98B51',
       'D_UID': 'DD2F078E-24C3-3782-9AC8-2031C758DB42',
       'D_HID': '0Sc6zebmt6H+YcSirXHDUI58e7OOEUdK+YXjYGSjM00'
    }
    single_url = 'http://listings.findthecompany.com/distil_identify_cookie.html?uid=DD2F078E-24C3-3782-9AC8-2031C758DB42&d_ref=/ajax_search&qs=?_len=20&page=0&app_id=1662&_sortfld=sales_volume_us&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=_sphinx_universal_search&_fil%5B0%5D%5Boperator%5D=LIKE&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=apple&_fil%5B0%5D%5Bignore%5D=false&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=company_name&head%5B%5D=_GC_address&head%5B%5D=total_employees&head%5B%5D=employees_here&head%5B%5D=sales_volume_us&head%5B%5D=year_started&head%5B%5D=citystate&head%5B%5D=localeze_classification&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=name_state_tit&head%5B%5D=phys_address&head%5B%5D=phys_city&head%5B%5D=phys_state&head%5B%5D=phys_country_code'

    # single_url = "http://listings.findthecompany.com/distil_identify_cookie.html?uid=45CEBDBD-7C65-3288-A684-BC083F8E0CC8&d_ref=/ajax_search&qs=?_len=20&page=0&app_id=1662&_sortfld=sales_volume_us&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=_sphinx_universal_search&_fil%5B0%5D%5Boperator%5D=LIKE&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=apple&_fil%5B0%5D%5Bignore%5D=false&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=company_name&head%5B%5D=_GC_address&head%5B%5D=total_employees&head%5B%5D=employees_here&head%5B%5D=sales_volume_us&head%5B%5D=year_started&head%5B%5D=citystate&head%5B%5D=localeze_classification&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=name_state_tit&head%5B%5D=phys_address&head%5B%5D=phys_city&head%5B%5D=phys_state&hea+d%5B%5D=phys_country_code"




    def start_requests(self):

      # for url in self.start_urls:
          meta={'handle_httpstatus_list': [416, 302, 404, 409]}
          print "........", self.single_url
          yield Request(url=self.single_url, headers=self.headers, cookies=self.cookies,
                        meta=meta, callback=self.test_function)


    #
    # def parse(self, response):
    #     # doc = html.fromstring(response.body)
    #     print "...........", response.url
    #
    #     url = "http://www.findthecompany.com/"
    #     yield Request(url=url, method='GET', headers=self.headers,cookies=self.cookies,
    #               callback=self.test_function)




    def test_function(self, response):
      print ">>22222222222222222222", response.url
      item = items.EmployeeDetailsItem()
      item['name'] = response.url
      yield item
      print 'jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj'
      # data = json.loads(response.body)
      # print ">>>>>>>>>>>>>>>>>>>", data
      item['given_city'] = response.body
      yield item
      # urls = 'http://listings.findthecompany.com/?launch_filters=%5B%7B%22field%22%3A%22company_name%22%2C%22operator%22%3A%22LIKE%22%2C%22value%22%3A%22BALLARD%22%7D%5D'
      # urls = "http://listings.findthecompany.com/ajax_search?_len=20&page=0&app_id=1662&_sortfld=sales_volume_us&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=_sphinx_universal_search&_fil%5B0%5D%5Boperator%5D=LIKE&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=apple&_fil%5B0%5D%5Bignore%5D=false&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=company_name&head%5B%5D=_GC_address&head%5B%5D=total_employees&head%5B%5D=employees_here&head%5B%5D=sales_volume_us&head%5B%5D=year_started&head%5B%5D=citystate&head%5B%5D=localeze_classification&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=name_state_tit&head%5B%5D=phys_address&head%5B%5D=phys_city&head%5B%5D=phys_state&head%5B%5D=phys_country_code"
      urls = "http://listings.findthecompany.com/ajax_search?_len=20&page=0&app_id=1662&_sortfld=sales_volume_us&_sortdir=DESC&_fil%5B0%5D%5Bfield%5D=_sphinx_universal_search&_fil%5B0%5D%5Boperator%5D=LIKE&_fil%5B0%5D%5Boptional%5D=false&_fil%5B0%5D%5Bvalue%5D=apple&_fil%5B0%5D%5Bignore%5D=false&_tpl=srp&head%5B%5D=_i_1&head%5B%5D=company_name&head%5B%5D=_GC_address&head%5B%5D=total_employees&head%5B%5D=employees_here&head%5B%5D=sales_volume_us&head%5B%5D=year_started&head%5B%5D=citystate&head%5B%5D=localeze_classification&head%5B%5D=id&head%5B%5D=_encoded_title&head%5B%5D=name_state_tit&head%5B%5D=phys_address&head%5B%5D=phys_city&head%5B%5D=phys_state&head%5B%5D=phys_country_code"
      yield Request(url=urls, callback=self.parse_Companies_by_industry,  method='GET', headers=self.headers,
                    cookies=self.cookies,meta = {'handle_httpstatus_list':[416,302, 404, 409]},dont_filter=True)


    def parse_Companies_by_industry(self, response):
        print ">>inside parse companieeeeeeeeeeeee", response.url
        item = items.EmployeeDetailsItem()
        # doc = html.fromstring(response.body)
        # name = doc.xpath('.//h1[@class="stnd-page-title"]/text()')
        item['employee_address'] = response.url
        item['employee_state'] = response.body
        yield item



