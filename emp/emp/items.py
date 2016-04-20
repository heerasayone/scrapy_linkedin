
import scrapy
from scrapy.item import Item, Field

class EmployeeDetailsItem(Item):
  name = Field()
  designation = Field()
  phone_no = Field()
  email_id = Field()
  employee_address = Field()
  linkedin_id = Field()
  company_name = Field()
  employee_city = Field()
  employee_state = Field()
  employee_street = Field()
  given_street = Field()
  given_state = Field()
  given_city = Field()

