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
    name = "corporationwiki2"
    domain = "https://www.corporationwiki.com"
    start_urls = ["https://www.corporationwiki.com/"]
    listing_url = "https://www.corporationwiki.com/search/results?term={company_name}"
    download_delay = 10

    def parse(self, response):
        f = resource_stream('emp', 'second_16_32.csv')
        SIGNED_KEY = f.read()
        single_company_list = SIGNED_KEY.split('\n')
        for company in single_company_list:
          flag = 0
          if company:
            company_name = company.split(',')[1]
            company_city = company.split(',')[6]
            state = company.split(',')[8]
            company_street = company.split(',')[5]
            new_name = company_name.replace(' ','%20')
            listing_url = self.listing_url.format(company_name=new_name)
            meta = {"company_name": company_name, "company_city": company_city, "company_street":company_street,
            "url": listing_url}
            # url = 'https://www.corporationwiki.com/search/results?term=BALLARD%20INC'
            # meta = {"company_name": 'BALLARD INC', "company_city": 'BARDSTOWN', "company_street":'128 BANJO STREET',
            #         'url': url}
            yield Request(url=listing_url, callback=self.parse_listing_page, meta=meta)


    def parse_listing_page(self, response):
        doc = html.fromstring(response.body)
        meta = response.meta
        compnay_city = meta['company_city']
        company_name = meta['company_name']
        company_street = meta['company_street']
        if 'listing_count' not in meta:
          listing_count = doc.xpath('.//fieldset[@id="entity_type_facets_container"]//span/text()')
          if listing_count:
            if int(listing_count[0]) <= 1000:
              listing_count = listing_count[0]
        else:
          listing_count = meta['listing_count']
        company_urls = doc.xpath('.//table[@class="table table-striped"]//tr')
        for company_url in company_urls[:-1]:
            company_name = company_url.xpath('.//td[@valign="top"]/a/text()')[0]
            company_address_list = company_url.xpath('.//td[@valign="top"]/text()')
            company_address = self._remove_special_characters(company_address_list)
            city,state = self.pasrse_address(company_address[0])
            if compnay_city.lower().strip() == city.lower().strip():
                company_url = company_url.xpath('.//td[@valign="top"]/a/@href')[0]
                yield Request(url=self.domain+company_url, callback=self.parse_single_company, meta=meta)
                break

        #pagination
        if listing_count:
          if int(listing_count) > 10:
            listing_count = int(listing_count)-10
            meta['listing_count'] = listing_count
            count = int(listing_count)/10
            for i in range(1,count):
              listing = meta['url']+'&page='+str(i)
              yield Request(url=listing, callback=self.parse_listing_page, meta=meta)

    def parse_single_company(self, response):
        doc = html.fromstring(response.body)
        meta = response.meta
        employees_list = doc.xpath('.//div[@itemprop="employee"]')
        for employee_list in employees_list:
            item = items.EmployeeDetailsItem()
            item['name'] = employee_list.xpath('.//span[@itemprop="name"]/text()')
            item['designation'] = employee_list.xpath('.//span[@itemprop="jobTitle"]/text()')
            item['company_name'] = meta['company_name']
            item['given_city'] = meta['company_city']
            item['given_street'] = meta['company_street']
            yield item

    def pasrse_address(self, address):
        city_state = address.split(',')
        city = city_state[0].strip()
        state = city_state[-1].strip()
        return city, state

    def _remove_special_characters(self, datas):
        """
        Removes special characters from the inout data
        :param data: String
        :return: String
        """
        data_list = []
        for data in datas:
            un_wanted_characters = ['\n', '\xae', '\t', '\r']
            for special_character in un_wanted_characters:

              data = re.sub(special_character, '', data)
            data_list.append(data)
        new_list =  self._remove_nul_strings(data_list)
        return new_list

    def _remove_nul_strings(self, data):
        """
        Removes null characters from the input list
        :param data:
        :return: List
        """
        data = ([s.strip(' ') for s in data])
        new_string = filter(None, data)
        return new_string
