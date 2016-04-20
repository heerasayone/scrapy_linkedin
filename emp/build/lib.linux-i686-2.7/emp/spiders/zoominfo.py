import scrapy
import re
import csv
import string
from lxml import html
from scrapy.http import Request
from ..import items
from pkg_resources import resource_stream

include_package_data = True


class Employee_details(scrapy.Spider):
    name = "zoominfo"
    domain = "http://www.zoominfo.com"
    start_urls = ["http://www.zoominfo.com/"]
    search_url = 'http://www.zoominfo.com/s/search/company'
    single_company_url = 'http://www.zoominfo.com/c/{company_id}'
    # form_data = 'criteria=%7B%22companyName%22%3A%7B%22value%22%3A%22BALLARD%20INC%22%2C%22isUsed%22%3Atrue%7D%7D&isCountOnly=false'
    form_data = 'criteria=%7B%22companyName%22%3A%7B%22value%22%3A%22{company_name}%22%2C%22isUsed%22%3Atrue%7D%7D&isCountOnly=false'

    # start_urls = ["http://www.zoominfo.com/c/Mayor-Logistics-Inc/366258392"]
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    download_delay = 5

    def parse(self, response):
        doc = html.fromstring(response.body)
        s=0
        f = resource_stream('emp', 'companies1.csv')

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
            meta = {"company_name": company_name, "company_city": company_city, "company_street":company_street}
            form_new_data = self.form_data.format(company_name=new_name)
            yield Request(url=self.search_url, method='POST', body=form_new_data, headers=self.headers,
                      callback=self.parse_Companies_by_industry, meta=meta)


        # yield Request(url='http://www.zoominfo.com/p/Anthony-Cocuzzo/1476884805', callback=self.parse_employee_address)

    def parse_Companies_by_industry(self, response):
        doc = html.fromstring(response.body)
        meta = response.meta
        company_urls = doc.xpath('.//a[@class="companyResultsName"]/@href')
        for company_url in company_urls:
            company_id = re.search(r'companyId=(.+)&',company_url)
            if company_id:
                company_page_url = self.single_company_url.format(company_id=company_id.group(1))

                yield Request(url=company_page_url, callback=self.parse_companies, meta=meta)


    def parse_companies(self, response):
        doc = html.fromstring(response.body)
        flag = 0
        meta = response.meta
        employees_list = doc.xpath('.//div[@class="companyContactNames"]//div[@class="contactItem"]')
        if employees_list:
            name = doc.xpath('.//div[@class="dataSection companyTitle"]/h1/text()')
            street = doc.xpath('.//span[@class="street"]/text()')
            city = doc.xpath('.//span[@class="city"]/text()')
            state = doc.xpath('.//span[@class="state"]/text()')
            if street:
              if street[0].lower() == meta['company_street'].lower():
                  meta['street'] = street[0]
                  flag = 1
              else:
                if city:
                  if city[0].lower() == meta['company_city'].lower():
                    meta['city'] = city[0]
                    flag = 1
            elif city:
              if city[0].lower() == meta['company_city'].lower():
                meta['city'] = city[0]
                flag = 1
            if flag == 1:
                employees_list = doc.xpath('.//div[@class="companyContactNames"]//div[@class="contactItem"]')
                for employee in employees_list:
                   employee_name = employee.xpath('.//a[@class="pivotContactName"]/text()')[0].strip()
                   designation = employee.xpath('.//div[@class="companyContactTitle"]/text()')
                   employee_url = employee.xpath('.//a[@class="pivotContactName"]/@href')[0]
                   meta['employee_name'] = employee_name
                   meta['designation'] = designation
                   yield Request(url=employee_url, callback=self.parse_employee_address, meta=meta)

    def parse_employee_address(self, response):
        doc = html.fromstring(response.body)
        item = items.EmployeeDetailsItem()
        meta = response.meta
        address = doc.xpath('.//div[@class="localAddress"]//i/text()')
        name = doc.xpath('.//div[@class="personSummary"]//h1[@itemprop="name"]/text()')
        name2 = doc.xpath('.//h1[@id="fullName"]/text()')
        if address:
            address = self._remove_special_characters(address)
            if ',' in address[0]:
                addr = address[0].split(',')
                address = addr[0].strip()+','+addr[1].strip()
            item['employee_address'] = address
            # item['employee_state'] = addr[1].strip()
        if name:
          item['name'] = name[0].strip()
          item['company_name'] = meta['company_name']
          item['given_city'] = meta['company_city']
          item['given_street'] = meta['company_street']
          item['designation'] = meta['designation'][0]
        elif name2:
          item['name'] = name2[0].strip()
          item['company_name'] = meta['company_name']
          item['given_city'] = meta['company_city']
          item['given_street'] = meta['company_street']
          item['designation'] = meta['designation'][0]
          yield item



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
        print "llllllllllllll", new_list
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
