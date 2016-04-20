import scrapy
import csv
import string
from lxml import html
from scrapy.http import Request
from ..import items
from pkg_resources import resource_stream

include_package_data = True


class Employee_details(scrapy.Spider):
    name = "manta"
    domain = "http://www.manta.com"
    # start_urls = ["http://www.manta.com"]
    # start_urls = ["http://www.forever21.com/IN/Product/Main.aspx?br=f21"]
    company_url = "http://www.manta.com/search?search_source=nav&pt=&search_location=+&search={company_name}"
    download_delay = 5
    # headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #            'Accept-Encoding':'gzip,deflate,sdch',
    #            'Accept-Language':'en-US,en;q=0.8',
    #            'Cache-Control':'max-age=0',
    #            'Connection':'keep-alive',
    #            'Host':'www.manta.com',
    #            'user-agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'}

    headers = {
      'Connection': 'keep-alive',
      'Content-Encoding': 'gzip',
      'Content-Type': 'text/html; charset=utf-8',
      # 'Date': 'Mon, 11 Apr 2016 06:39:22 GMT',
      # 'Server': 'nginx',
      'Transfer-Encoding': 'chunked',
      'Vary': 'Accept-Encoding, Accept-Encoding',
      'X-Distil-CS': 'MISS',
      'X-Response-Time': '40ms',
      'cache-control': 'no-cache',
      'x-powered-by': 'Express'
    }

    cookies = {
      'C3S-249': 'on',
      'C3UID': '5390251961460348697',
      'C3UID-249': '5390251961460348697',
      'D_HID': 'fG0A0bWWeQNw3gbCDuZSS9B2b797j+qVfJ7tkqdNOyk',
      'D_IID': 'EF5267B7-C7D0-3114-9F32-68C72BEC5B1B',
      'D_PID': '83606733-E95D-3A79-89BC-0894730FBB78',
      'D_SID': '182.75.158.122:8OM1iwInmfoO8D3atxZSqplsO0ULYD7o3PwOd9GOYUs',
      'D_UID': '85070DE7-E0ED-3A70-B216-17BAFAE7CD27',
      '__gads': 'ID=927823d0016e6266:T=1460350780:S=ALNI_MZoBYVrR0CBemOtcoUHOMsBaQ_N5Q',
      '_dc_gtm_UA-10299948-11':'1',
      '_ga': 'GA1.2.542908633.1460348696',
      '_ok': '7187-253-10-6096',
      '_okbk': 'cd4%3Dtrue%2Cvi5%3D0%2Cvi4%3D1460348702569%2Cvi3%3Dactive%2Cvi2%3Dfalse%2Cvi1%3Dfalse%2Ccd8%3Dchat'
               '%2Ccd6%3D0%2Ccd5%3Daway%2Ccd3%3Dfalse%2Ccd2%3D0%2Ccd1%3D0%2C',
      '_okdetect': '%7B%22token%22%3A%2214603486996260%22%2C%22proto%22%3A%22http%3A%22%2C%22host%22%3A%22www.manta'
                   '.com%22%7D',
      '_oklv': '1460358075513%2CBNnerKfjbgF8M59G696VP36aCJ0E3oar',
      'cust_id':'fd3fca44-3626-4df0-ae5c-ceabe1b1e936',
      'ftoggle-frontend-prod':'%7B%22e%22%3A1%2C%22v%22%3A239%2C%22trackingNumber%22%3A%7B%22e%22%3A1%7D%2C%22olark'
                              '%22%3A%7B%22e%22%3A1%2C%22chat%22%3A%7B%22e%22%3A1%7D%7D%2C%22homeyou%22%3A%7B%22e%22%3A1%7D%2C%22listing_manager_99%22%3A%7B%22e%22%3A1%7D%2C%22yext%22%3A%7B%22e%22%3A1%2C%22interstitial%22%3A%7B%22e%22%3A1%2C%22edit%22%3A%7B%22e%22%3A1%7D%2C%22view%22%3A%7B%22e%22%3A1%7D%2C%22product%22%3A%7B%22e%22%3A1%7D%2C%22stats%22%3A%7B%22e%22%3A1%7D%7D%7D%2C%22abTests%22%3A%7B%22e%22%3A1%2C%22engagement%22%3A%7B%22e%22%3A1%2C%22no_test%22%3A%7B%22e%22%3A1%7D%7D%7D%2C%22froyo%22%3A%7B%22e%22%3A1%7D%2C%22surveys%22%3A%7B%22e%22%3A1%7D%2C%22tests%22%3A%7B%22e%22%3A1%7D%2C%22enhancedStats%22%3A%7B%22e%22%3A1%2C%22basicEnhancedStats%22%3A%7B%22e%22%3A1%7D%2C%22fullEnhancedStats%22%3A%7B%22e%22%3A1%7D%2C%22newGraphLayout%22%3A%7B%22e%22%3A1%7D%7D%2C%22olarkWelcomeMessage%22%3A%7B%22e%22%3A1%2C%22olark_stats_prompt_a%22%3A%7B%22e%22%3A1%7D%7D%2C%22PPC%22%3A%7B%22e%22%3A1%2C%22add_builder%22%3A%7B%22e%22%3A1%7D%7D%2C%22newCompanyCatcher%22%3A%7B%22e%22%3A1%7D%2C%22offHoursScan%22%3A%7B%22e%22%3A1%7D%2C%22daytimeScan%22%3A%7B%22e%22%3A1%2C%22control%22%3A%7B%22e%22%3A1%7D%7D%2C%22mixpanel%22%3A%7B%22e%22%3A1%7D%7D',
      'hblid':'ugMlcst6iSte1zsT696VP36aCJE06oBa',
      'manta_session': '%7B%22loginIp%22%3A%2210.78.37.106%22%2C%22subId%22%3A%22%22%2C%22touchTimestamp%22%3A'
                       '%221460356730900%22%2C%22userRole%22%3A%22%22%7D',
      'mp_f6712b90922aca648f9e2307427ca86f_mixpanel':
        '%7B%22distinct_id%22%3A%20%221540390503230-0b45c4db-30263348-100200-15403905033372%22%2C%22offHours%22%3A%20true%2C%22treatment%22%3A%20%22engagement_no_test%22%2C%22%24initial_referrer%22%3A%20%22http%3A%2F%2Fwww.manta.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.manta.com%22%7D',
      'mp_mixpanel__c': '17',
      'olfsk': 'olfsk5850871601141989',
      'refer_id': '7777',
      'viewedOuibounceModal':'true',
      'wcsid': 'BNnerKfjbgF8M59G696VP36aCJ0E3oar',
    }

    def start_requests(self):
        url = 'http://www.manta.com'

        yield Request(url=url, headers=self.headers,cookies=self.cookies, callback=self.parse_company_list)

    def parse_company_list(self, response):
        doc = html.fromstring(response.body)
        print ">>>>>>>>", response.url
        #
        # f = resource_stream('employee_details', 'companies.csv')
        # SIGNED_KEY = f.read()
        # single_company_list = SIGNED_KEY.split('\n')
        # for company in single_company_list:
        #   if company:
        #     company_name = company.split(',')[2]
        #     company_city = company.split(',')[4]
        #     # state = company.split(',')[5]
        #     street = company.split(',')[3]
        #     meta = {'company_name' : company_name, 'company_city': company_city,'street': street}
        #     new_name = company_name.replace(' ', '+')
        #     company_name_url = new_name.replace('&', '%26')
        #     name = self.company_url.format(company_name=company_name_url)
        #     yield Request(url=name,callback=self.parse_companies, meta=meta)



        # yield Request(url='http://www.manta.com/c/mm2r3nr/brad-cole-construction-co-inc',
        #               callback=self.parse_employees)
        # yield Request(url='http://www.manta.com/search?search_source=nav&pt=&search_location=+&search=BRAD+COLE+CONSTRUCTION+CO+INC',
        #               callback=self.parse_companies,
        #               meta = {'company_name' : 'BRAD COLE CONSTRUCTION CO INC', 'company_city': 'CARROLLTON','street': '2250 LOVVORN RD'})

    def parse_companies(self, response):
        meta = response.meta
        doc = html.fromstring(response.body)
        company_names = doc.xpath('.//div[@class="media-body"]')
        for company in company_names:
            company_url = company.xpath('.//a[@itemprop="name"]/@href')[0]
            c_city = company.xpath('.//div[@itemprop="address"]//span[@itemprop="addressLocality"]/text()')
            c_street = company.xpath('.//div[@itemprop="address"]//span[@itemprop="streetAddress"]/text()')
            c_state = company.xpath('.//div[@itemprop="address"]//span[@itemprop="addressRegion"]/text()')
            company_name = company.xpath('.//a[@itemprop="name"]//strong/text()')[0].strip()
            street = meta['street']
            city = meta['company_city']

            if len(company_names)>1:
              if c_street:
                if c_street[0].lower() == street.lower():
                  meta['c_street'] = c_street
                  meta['c_city'] = c_city
                  yield Request(url=self.domain+company_url, meta=meta, callback=self.parse_employees)
                else:
                  if c_city:
                    if city.lower() == c_city[0].lower():
                      meta['c_city'] = c_city
                      yield Request(url=self.domain+company_url, meta=meta, callback=self.parse_employees)
              else:
                if c_city:
                  if city.lower() == c_city[0].lower():
                    meta['c_city'] = c_city
                    yield Request(url=self.domain+company_url, meta=meta, callback=self.parse_employees)
            else:
              if company_name.lower == meta['company_name']:
                yield Request(url=self.domain+company_url, meta=meta, callback=self.parse_employees)


            # meta = {'c_city': c_city, 'c_street': c_street, 'c_state': c_state }
            # if c_street:
            # if city.lower() == c_city.lower():
            #   if c_street[0].lower() == street.lower():
            # company_name = company.xpath('.//strong/text()')[0].strip()
            # print ".............", company_url
            # meta = {'company_name': company_name}
            #    yield Request(url=self.domain+company_url, meta=meta, callback=self.parse_employees)

    def parse_employees(self, response):
        doc = html.fromstring(response.body)
        meta = response.meta
        employees_list = doc.xpath('.//li[@itemprop="employee"]')
        for employee in employees_list:
            item = items.EmployeeDetailsItem()
            name = employee.xpath('.//span[@itemprop="name"]//strong/text()')
            if name:
                item['name'] = name[0]
            else:
                item['name'] = employee.xpath('.//span[@itemprop="name"]//a/text()')
            item['designation'] = employee.xpath('.//span[@itemprop="jobTitle"]/text()')
            item['phone_no'] = employee.xpath('.//span[@itemprop="telephone"]/text()')
            item['email_id'] = employee.xpath('.//span[@itemprop="email"]/text()')
            item['company_name'] = meta['company_name']
            if 'c_city' in meta:
              item['city'] = meta['c_city']
            # item['state'] = meta['c_state']
            if 'c_street' in meta:
              item['street'] = meta['c_street']
            item['given_street'] = meta['street']
            # item['main_state'] = meta['state']
            item['given_city'] = meta['company_city']
            yield item


    def _apply_schema_to_url(self, url):
        """
        Applies schema to urls fed.
        :param url: String
        :return: String
        """
        if "http:" in url:
          return url
        else:
          return "http:" + url
