#! /usr/env/bin python3
# -*- encoding utf-8 -*-

"""
------------------------------------------------------------------------------
    filings.py   |    get company filings from SEC's Edgar webiste
------------------------------------------------------------------------------

Author   : Simone Santoni, simone.santoni.1@city.ac.uk

Synopsis : Selenium-based workflow to get various types of filings from SEC's
           Edgar webiste
          
Status   : Alpha version

"""

# %% libraries
import os
import glob
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

# %% params
company_name = "jpmorgan"
filing_type = "proxy"
from_to = ["2000-01-01", "2021-06-30"]
gecko_driver = r"/opt/selenium/bin/geckodriver"
destination_folder = "/home/simone/filings/"
target_url = "https://www.sec.gov/"

# %% initialize driver and visit the target webpage
# storing data
os.chdir(destination_folder)
# company level folder
if os.path.exists(company_name):
    pass
else:
    os.mkdir(company_name)
# navigate to the company folder
os.chdir(company_name)
# folders with the documents
if os.path.exists(filing_type):
    pass
else:
    os.mkdir(filing_type)
# set current directory
os.chdir(filing_type)
# initialize a driver
driver = webdriver.Firefox(executable_path=gecko_driver)
# visit SEC's Edgar website
url = target_url
driver.get(url)

# %% select filing type
# fix xpath
if filing_type == "10-k":
    xpath_0 = "/html/body/main/div[4]/div[2]/div[3]/h5"
    xpath_1 = "/html/body/main/div[4]/div[2]/div[3]/div/button[1]"
elif filing_type == "proxy":
    xpath_0 = "/html/body/main/div[4]/div[2]/div[4]/h5"
    xpath_1 = "/html/body/main/div[4]/div[2]/div[4]/div/button[1]"
else:
    print(
        """
          Please select one of the following filing types:
          
          -'10-k'
          -'proxy'
          
          """
    )
# pick-up filing type
to_click = driver.find_element_by_xpath(xpath_0)
to_click.click()
time.sleep(5)
# visualize filing type
to_click = driver.find_element_by_xpath(xpath_1)
to_click.click()
time.sleep(5)
# filter-in target reports
filter_in = driver.find_element_by_xpath('//*[@id="searchbox"]')
filter_in.send_keys(filing_type)
filter_in.send_keys(Keys.RETURN)
# timespan for the search
xpaths = ['//*[@id="filingDateFrom"]', '//*[@id="filingDateTo"]']
for xpath, date in zip(xpaths, from_to):
    item = driver.find_element_by_xpath(xpath)
    item.clear()
    item.send_keys(date)
    item.send_keys(Keys.RETURN)

# %% download summary
to_click = driver.find_element_by_xpath(
    "/html/body/main/div[5]/div/div[3]/div[1]/button[2]/span"
)
to_click.click()
# move file to desired folder
to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.csv"))[0]
out_f = "{}_summary.csv".format(filing_type)
os.rename(to_move, os.path.join(".", out_f))

# %% download json file
# open file in a new tab
to_click = driver.find_element_by_xpath("//*[@id=\"dataSource\"]")
to_click.click()
handles = driver.window_handles
driver.switch_to.window(handles[1])
# get raw data
to_click = driver.find_element_by_xpath("//*[@id=\"rawdata-tab\"]")
to_click.click()
# make the soup and extrct the json file
soup = BeautifulSoup(driver.page_source)
contents = json.loads(soup.find("pre", {"class": "data"}).get_text())
# write the json file to a lcoal file
out_f = os.path.join('.', 'metadata.json')
with open(out_f, 'w') as pipe:
    json.dump(contents, pipe)
# get back to search page
driver.switch_to.window(handles[0])

# %% download documents
# links
links = driver.find_elements_by_xpath(
    "/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody//td[2]/div/a[1]"
)
# %% repoting dates
reporting_dates = []
for i in range(len(links)):
    table = '/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody'
    row = 'tr[{}]'.format(i+1)
    col = 'td[4]/a'
    xpath = '/'.join([table, row, col])
    item = driver.find_element_by_xpath(xpath).text
    reporting_dates.append(item)  
# %% iterate over documents
# open documents
for link, date in zip(links, reporting_dates):
    # open the page
    link.click()
    # wait to fully load the page
    time.sleep(10)
# %% save documents
# container for the download details
download_summary = {}
# get the set of newly opened windows
handles = driver.window_handles
new_tabs = handles[1:]
for i, tab in enumerate(new_tabs):
    # navigate to the tab
    driver.switch_to.window(tab)
    # get url
    url = driver.current_url
    # get file type
    file_type = url[-4:]
    if (file_type is not 'json') & (file_type is not 'lank'):
        # populate download summary
        download_summary[i] = {'url': url, 'file_type': file_type}
        # save contents
        out_f = '{}{}'.format(i, file_type)
        with open(out_f, 'w') as pipe:
            pipe.write(driver.page_source)
    else:
        pass
# write download summary to file
with open('download_summary.json', 'w') as pipe:
    json.dump(download_summary, pipe)

# %%
# That's all folks!
