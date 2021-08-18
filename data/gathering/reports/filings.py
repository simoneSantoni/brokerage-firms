#! /usr/env/bin python3
# -*- encoding utf-8 -*-

"""
------------------------------------------------------------------------------
    filings.py   |    get 10-k modules from SEC's Edgar webiste
------------------------------------------------------------------------------

Author   :

Synopsis :

Status   :

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
filing_type = "10-k"
from_to = ["2000-01-01", "2021-06-30"]
gecko_driver = r"/opt/selenium/bin/geckodriver"
destination_folder = "/home/simone/filings/"
target_url = "https://www.sec.gov/"

# %% initialize driver and visit the target webpage
# storing data
os.chdir(destination_folder)
#os.mkdir(company_name)
os.chdir(company_name)
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
    xpath_0 = ""
    xpath_1 = ""
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
if filing_type == "10-k":
    filter_in = driver.find_element_by_xpath('//*[@id="searchbox"]')
    filter_in.send_keys(filing_type)
    filter_in.send_keys(Keys.RETURN)
else:
    pass
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
    "/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody//td[4]/a"
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
#TODO: broken, adjust
for link, date in zip(links, reporting_dates):
    # refesh links
    #links = driver.find_elements_by_xpath(
    #"/html/body/main/div[5]/div/div[3]/div[3]/div[2]/table/tbody//td[4]/a")
    # open the page
    links[i].click()
    # save the file
    out_f = '{}.html'.format(date)
    with open(out_f, 'w') as pipe:
        pipe.write(driver.page_source)
    # get back to search page
    driver.switch_to.window(handles[0])
    #driver.close()
    #time.sleep(12)
    ## rename file
    #to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))[0]
    #out_f = "{}_{}_{}.pdf".format(year_, j, i)
    #os.rename(to_move, os.path.join('.', out_f))


# %% !!!!!!!!!!!!!!!!!!!!!!!!! dirty stuff !!!!!!!!!!!!!!!!!!!!!!!!!!!
