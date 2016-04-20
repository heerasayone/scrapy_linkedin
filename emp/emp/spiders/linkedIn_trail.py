import scrapy
import re
import csv,math
import requests
import time
import json
from lxml import html
from scrapy.http import Request, FormRequest
from ..import items
from pkg_resources import resource_stream
from selenium import webdriver
import random
import urllib2
# import requests

include_package_data = True

# header = {'Referer':''}


class Employee_details(scrapy.Spider):
    name = "linkedin1"
    domain = "https://www.linkedin.com"
    start_urls = ["https://www.linkedin.com"]
    # company_search_url = 'https://www.linkedin.com/vsearch/c?type=companies&keywords=BAKERSFIELD+PIPE+%26+SUPPLY+INC&'
    company_search_url ="https://www.linkedin.com/vsearch/c?type=companies&keywords={company_name}&"
    i = 0
    ss = 0
    # download_delay = 5

    fieldnames = ['Name', 'Designation', 'Address', 'Linkedin_id', 'Company_name', 'Given_street', 'Given_city']

#     headers = {
#       'host':'www.linkedin.com',
#       'method':'GET',
#       'path':'/vsearch/c?type=companies&keywords=legal_name&',
#       'scheme':'https',
#       'version:HTTP/1.1
# accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# accept-encoding:gzip,deflate,sdch
# accept-language:en-US,en;q=0.8
# cache-control:max-age=0
#     }

  
# formdata={'session_key': 'inside.out4001@gmail.com', 'session_password': 'insideout4001',
#                                   'csrfToken': csrftoken},

    # def process_reqeust(self, reqeust):
    #
    #     http_proxy = "http://188.211.26.96:60000"
    #     https_proxy = "https://188.211.26.96:60000"
    #
    #     proxyDict = {
    #         "http"  : http_proxy,
    #         "https" : https_proxy
    #     }
    #     reqeust.meta['proxies'] = proxyDict
    #     return reqeust.meta



    def parse(self, response):

        doc = html.fromstring(response.body)
        meta = {'handle_httpstatus_list': [302], 'dont_redirect': True}
        csrftoken = doc.xpath('.//input[@name="csrfToken"]/@value')
        return [FormRequest.from_response(response,
                        formdata={'session_key': 'remidavid45@gmail.com', 'session_password': 'remi12345',
                                  'csrfToken': csrftoken},
                        callback=self.after_login, formxpath='.//form[@class="login-form"]', meta=meta)]


    def after_login(self, response):
        meta = response.meta.copy()

        f = resource_stream('emp', 'companies1.csv')
        SIGNED_KEY = f.read()
        single_company_list = SIGNED_KEY.split('\n')
        for company in single_company_list:
          if company:
            company_name = company.split(',')[1]
            company_city = company.split(',')[6]
            state = company.split(',')[8]
            company_street = company.split(',')[5]
            company_zip = company.split(',')[9]
            meta['company_name'] = company_name
            meta['company_city'] = company_city
            meta['company_street'] = company_street
            meta['company_zip'] = company_zip
            #
            # meta = {'company_name': "TERRELL'S OFFICE MACHINES INC.", 'company_city': "BOZEMAN",'company_street': "215 HAGGERTY LN",
            #         'company_zip': "59715" }
            new_name = company_name.replace(' ', '+')
            company_name_url = new_name.replace('&', '%26')
            name = self.company_search_url.format(company_name=company_name_url)
            # name = "https://www.linkedin.com/vsearch/c?type=companies&keywords=TERRELL%27S+OFFICE+MACHINES+INC&"
            yield Request(url=name, callback=self.parse_companies, meta=meta, dont_filter=True)


    def parse_companies(self, response):
        #self.excecute_random_event_matrix()
        meta = response.meta.copy()
        company_list_json = re.search(r';\"><!--(.+)--></code>',response.body, re.DOTALL)
        if company_list_json:
            data = json.loads(company_list_json.group(1))
            company_list = data['content']['page']['voltron_unified_search_json']['search']['results']
            if len(company_list) > 1:
              for company in company_list:
                  self.ss = self.ss+1
                  company_name = company['company']['fmt_canonicalName']
                  nn = company_name.replace('<B>','')
                  nnn = nn.replace('</B>','')
                  # if nnn.lower() == meta['company_name'].lower():
                  company_url = company['company']['link_biz_overview_6']
                  # meta['company_name'] = company_name
                  time.sleep(6)
                  yield Request(url=self.domain+company_url, callback=self.parse_single_company, meta=meta, dont_filter=True)

                  # else:
                  #   with open('new_linkedin_unmatched_list.csv', 'a') as csvfile3:
                  #     fieldnames = [meta['company_name']]
                  #     writer = csv.DictWriter(csvfile3, fieldnames=fieldnames)
                  #     writer.writeheader()

            elif len(company_list) == 1:
              company_url = company_list[0]['company']['link_biz_overview_6']
              yield Request(url=self.domain+company_url, callback=self.parse_single_company, meta=meta, dont_filter=True)



    def parse_single_company(self, response):
        #self.excecute_random_event_matrix()
        doc = html.fromstring(response.body)
        company_details_json = re.search(r'content\"><!--(.+?)--></code>',response.body)
        if company_details_json:
          company_details = json.loads(company_details_json.group(1))
          employee_page_url = re.search(r'\"employeeSearchUrl\"\:(.+?)\,\"companyType',response.body, re.DOTALL)
          meta = response.meta.copy()
          # street = doc.xpath('.//span[@class="street-address"]/text()')
          street = company_details['headquarters']['street1']
          # city = doc.xpath('.//span[@class="locality"]/text()')
          city = company_details['headquarters']['city']
          # zip_code = doc.xpath('.//span[@class="postal-code"]/text()')
          zip_code = company_details['headquarters']['zip']
          flag=0
          if street:
            # street = self._remove_special_characters(street)
            if street.lower().strip() == meta['company_street'].lower().strip():
                flag = 1
            else:
              if city:
                # city = self._remove_special_characters(city)
                if city.lower().strip() == meta['company_city'].lower().strip():
                  flag = 1
          elif city:
            # city = self._remove_special_characters(city)
            if city.lower().strip() == meta['company_city'].lower().strip():
              flag = 1
          elif zip_code:
            if zip_code[0].split('-')[0] == meta['company_zip']:
              flag = 1

          if flag == 1:
            employee_page_url = re.search(r'\"employeeSearchUrl\"\:\"(.+?)\"\,\"companyType',response.body, re.DOTALL)
            if employee_page_url:
                # company_employee_listing_url = re.search(r'href=\"(.+)">',employee_page_url.group(1), re.DOTALL)
                # if company_employee_listing_url:
                #     time.sleep(6)
              yield Request(url=employee_page_url.group(1), meta=meta,
                          callback=self.parse_employee_listing_page)

          if flag == 0:
            fieldnames = [meta['company_name']]
            with open('new_linkedin_unmatched_list.csv', 'a') as csvfile3:
              writer = csv.DictWriter(csvfile3, fieldnames=fieldnames)
              writer.writeheader()


    def parse_employee_listing_page(self, response):
        #self.excecute_random_event_matrix()
        meta = response.meta.copy()
        employee_list_json = re.search(r'\"results\"\:(.+)\,\"i18n_looking_for_someone\"',response.body, re.DOTALL)
        if employee_list_json:
          # ss = re.sub('\"distanceP\":\\u002d1\,',' ',employee_list_json.group(1))
          ss = employee_list_json.group(1).replace('\u002d1', '""', 20)
          datas = json.loads(ss)
          for employee in datas:
              if 'person' in employee:
                  if 'link_nprofile_view_4' in employee['person']:
                      employee_url = employee['person']['link_nprofile_view_4']
                      time.sleep(10)
                      yield Request(url=employee_url, callback=self.parse_employees, meta=meta)
                  elif 'link_nprofile_view_headless' in employee['person']:
                      employee_url = employee['person']['link_nprofile_view_headless']
                      time.sleep(7)
                      yield Request(url=employee_url, callback=self.parse_employees, meta=meta)

        # if 'pagination_count' not in meta:
          # meta['pagination_count'] = 0
        if 'pagination' not  in meta:
          pagination = re.search(r'\"resultCount\"\:(.+),\"company_search_link\"',response.body)
          meta['url'] = response.url

          if pagination:
            meta['pagination_count'] = int(pagination.group(1))
            meta['page_no'] = 1

        if 'pagination_count' in meta:
          if meta['pagination_count'] > 10:
            pagination_count = meta['pagination_count']
            meta['pagination_count'] = pagination_count - 10
            meta['pagination'] = ""
            page_no = meta['page_no'] + 1
            meta['page_no'] = page_no
            pagination_url = meta['url']+'&page_num={page_no}&'
            new_employee_url = pagination_url.format(page_no=page_no)
            time.sleep(9)
            yield Request(url=new_employee_url, meta=meta, callback=self.parse_employee_listing_page)


    def parse_employees(self, response):
        #self.excecute_random_event_matrix()
        self.i=self.i+1

        doc = html.fromstring(response.body)
        meta = response.meta
        name = doc.xpath('.//span[@class="full-name"]/text()')
        item = items.EmployeeDetailsItem()
        designation = doc.xpath('.//p[@class="title"]/text()')
        designation = ','.join(designation)
        address = doc.xpath('.//div[@id="location"]//span[@class="locality"]/a/text()')
        address = ','.join(address)
        linkedin_id = doc.xpath('.//a[@class="view-public-profile"]/text()')
        linkedin_id = ','.join(linkedin_id)
        company_name = meta['company_name']
        item['designation'] = doc.xpath('.//p[@class="title"]/text()')
        item['employee_address'] = doc.xpath('.//div[@id="location"]//span[@class="locality"]/a/text()')
        item['linkedin_id'] = doc.xpath('.//a[@class="view-public-profile"]/text()')
        item['company_name'] = meta['company_name']
        item['given_street'] = meta['company_street']
        item['given_city'] = meta['company_city']
        meta['item'] = item
        if name != ['LinkedIn Member']:
          item['name'] = name
          fieldnames = [name[0], designation, address, linkedin_id, company_name,meta['company_street'],meta['company_city'] ]
          with open('new_linkedin_items.csv', 'a') as csvfile1:
            writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
            writer.writeheader()
          yield item
        else:
          # new_get_name_link = doc.xpath('.//div[@class="katy-button-group button-group-primary"]//a/@href')[0]
          new_link = 'https://www.linkedin.com/premium/inmail/compose?destID={name_id}&'
          emp_id = doc.xpath('.//button[@data-page-type="full_page"]/@data-page-tracking-info')[0]
          name_id_dict = json.loads(emp_id)
          name_id = name_id_dict['vid']
          get_name_link = new_link.format(name_id=name_id)
          meta['item'] = item
          meta['designation'] = designation
          meta['address'] = address
          meta['linkedin_id'] = linkedin_id
          yield Request(url=get_name_link, callback=self.parse_name, meta=meta)


    def parse_name(self, response):
        doc = html.fromstring(response.body)
        meta = response.meta
        name = doc.xpath('.//a[@id="recip-mp-name"]/text()')
        item = meta['item']
        item['name'] = name
        fieldnames = [name[0], meta['designation'], meta['address'], meta['linkedin_id'], meta['company_name'], meta['company_street'],meta['company_city']]
        with open('new_linkedin_items.csv', 'a') as csvfile1:
          writer = csv.DictWriter(csvfile1, fieldnames=fieldnames)
          writer.writeheader()
        yield item

    def _remove_special_characters(self, data):
        """
        Removes special characters from the inout data
        :param data: String
        :return: String
        """
        if ',' in data[0]:
          data = data[0].replace(',','')
          return data
        else:
          return data[0]



