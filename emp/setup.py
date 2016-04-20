# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = emp.settings']},

    data_files = [("emp", ["/home/sayone/projects/emp/emp/first_1_16000.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/second_16_32.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/third_32_48.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/company_trail.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies2.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies3.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies4.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies5.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies6.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies7.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies8.csv"]),
                  ("emp", ["/home/sayone/projects/emp/emp/companies9.csv"])],
    include_package_data = True
)
