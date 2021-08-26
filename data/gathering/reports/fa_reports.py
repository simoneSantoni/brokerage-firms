#! /usr/env/bin python3
# -*- encoding utf-8 -*-

"""
------------------------------------------------------------------------------
    fa_reports.py   |    get company financial analyst reports from Mergent
------------------------------------------------------------------------------

Author   : Simone Santoni, simone.santoni.1@city.ac.uk

Synopsis : Selenium-based workflow to get search, retrieve, and download
           financial analyst reports 
         
Status   : Alpha version

"""

# %%
# lod libraries
#
import os, glob, shutil
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# %%
# arguments
#
# user, password
usr_, pwd_ = "sbbk475", "zeggan-xubto2-pEdzoh"
# company name
company_name = "jpm"
# lb, ub
year_ = 2000

# %%
# destination folder
#
# parent directory
os.chdir("/home/simone/faReports")
# company level folder
if os.path.exists(company_name):
    pass
else:
    os.mkdir(company_name)
os.chdir(company_name)

# %%
# initialize a driver
#
# local selenium
driver = webdriver.Firefox(executable_path=r"/opt/selenium/bin/geckodriver")
# remote selenium
# driver = webdriver.Remote(
#    command_executor="http://127.0.0.1:4444/wd/hub",
#    desired_capabilities=DesiredCapabilities.FIREFOX,
#    options=options
# )
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# options = webdriver.FirefoxOptions()
##options.add_argument('--headless')
# options.set_headless(headless=True)

# %%
# open investtext
#
# target
url = "https://0-www-mergentonline-com.wam.city.ac.uk/investextfullsearch.php"
driver.get(url)
# details for loging in
user = driver.find_element_by_xpath('//*[@id="extpatid"]')
user.send_keys(usr_)
pwd = driver.find_element_by_xpath("//*[@id='extpatpw']")
pwd.send_keys(pwd_)
# login
to_click = driver.find_element_by_xpath("//*[@id='submit']")
to_click.click()

# %%
# timespan search
#
lb = driver.find_element_by_xpath("//*[@id='textInRangeFrom']")
lb.send_keys("01/01/{}".format(year_))
ub = driver.find_element_by_xpath("//*[@id='textInRangeTo']")
ub.send_keys("12/31/{}".format(year_))

# %%
# company name
#
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[1]/td[2]/div/table/tbody/tr[1]/td[1]/a"
)
to_click.click()
name = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[2]/td/div/table/tbody/tr/td[4]/input"
)
name.send_keys(company_name)

# %%
# report type
#
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[1]/td[2]/div/table/tbody/tr[6]/td[1]/a"
)
to_click.click()
# --+ open choice menu
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[3]/a"
)
to_click.click()
# --+ get handles
time.sleep(2)
handles = {}
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    handles[handle] = driver.title
# --+ navigate to the choice menu
to_visit = ""
for key in handles.keys():
    if "Report Style" in handles[key]:
        to_visit = key
    else:
        pass
driver.switch_to.window(to_visit)
# --+ check box
time.sleep(2)
to_check = driver.find_element_by_xpath(
    "/html/body/div[3]/table/tbody/tr[3]/td[1]/input"
)
to_check.click()

# %%
# submit search
#
# get back to main window
driver.close()
to_visit = ""
for key in handles.keys():
    if "Mergent Online" in handles[key]:
        to_visit = key
    else:
        pass
driver.switch_to.window(to_visit)
# --+ submit search
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[6]/input"
)
time.sleep(6)
to_click.click()

# %%
# record the number of documents
#
docs = driver.find_element_by_xpath("//*[@id='matched1']").text
docs = int(docs.split(" ", 1)[0])

# %%
# go to the results page
#
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[4]/form/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td[8]/a[2]"
)
to_click.click()

# %%
# download the spreadsheet (it assumes Firefox downloads .xls as default)
#
to_click = driver.find_element_by_xpath("//*[@id='excellinkid']")
to_click.click()
summary = glob.glob(os.path.join("/home/simone/Downloads", "*.xls"))[0]
out_f = "{}_.xls".format(year_,)
os.rename(summary, os.path.join(".", out_f))

# %%
# download documents
# iterate over pages
# --+ first page
j = 1
links = driver.find_elements_by_xpath(
    "/html/body/div[6]/div[6]/table[2]/tbody//td[9]/a"
)
# ----+ iterate over links
for i, link in enumerate(links):
    # download file
    link.click()
    time.sleep(10)
    # rename/move file
    to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
    if len(to_move) > 0:
        out_f = "{}_{}_{}.pdf".format(year_, j, i)
        os.rename(to_move[0], os.path.join(".", out_f))
    else:
        time.sleep(10)
        # rename/move file
        to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
        if len(to_move) > 0:
            out_f = "{}_{}_{}.pdf".format(year_, j, i)
            os.rename(to_move[0], os.path.join(".", out_f))
        else:
            time.sleep(10)
            # rename/move file
            to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
            if len(to_move) > 0:
                out_f = "{}_{}_{}.pdf".format(year_, j, i)
                os.rename(to_move[0], os.path.join(".", out_f))
            else:
                time.sleep(10)
                # rename/move file
                to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
                if len(to_move) > 0:
                    out_f = "{}_{}_{}.pdf".format(year_, j, i)
                    os.rename(to_move[0], os.path.join(".", out_f))
                else:
                    time.sleep(60)
                    # rename/move file
                    to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
                    if len(to_move) > 0:
                        out_f = "{}_{}_{}.pdf".format(year_, j, i)
                        os.rename(to_move[0], os.path.join(".", out_f))
                    else:
                        pass
# ----+ clean folder
to_delete = glob.glob(os.path.join("/home/simone/Downloads", "*.*"))
if len(to_delete) > 0:
    for item in to_delete:
        os.remove(item)
    else:
        pass
# ----+ go to the next page
to_click = driver.find_element_by_xpath(
    "/html/body/div[6]/div[6]/table[1]/tbody/tr[2]/td[3]/span/a"
)
to_click.click()
# ----+ subsequent pages
while j <= int(docs / 25):
    # record paginations
    j += 1
    # get linksgg
    links = driver.find_elements_by_xpath(
        "/html/body/div[6]/div[6]/table[2]/tbody//td[9]/a"
    )
    # iterate over links
    for i in range(len(links)):
        # refresh links
        links = driver.find_elements_by_xpath(
            "/html/body/div[6]/div[6]/table[2]/tbody//td[9]/a"
        )
        # download file
        links[i].click()
        time.sleep(12)
        to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
        if len(to_move) > 0:
            out_f = "{}_{}_{}.pdf".format(year_, j, i)
            os.rename(to_move[0], os.path.join(".", out_f))
        else:
            time.sleep(10)
            # rename/move file
            to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
            if len(to_move) > 0:
                out_f = "{}_{}_{}.pdf".format(year_, j, i)
                os.rename(to_move[0], os.path.join(".", out_f))
            else:
                time.sleep(10)
                # rename/move file
                to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
                if len(to_move) > 0:
                    out_f = "{}_{}_{}.pdf".format(year_, j, i)
                    os.rename(to_move[0], os.path.join(".", out_f))
                else:
                    time.sleep(10)
                    # rename/move file
                    to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
                    if len(to_move) > 0:
                        out_f = "{}_{}_{}.pdf".format(year_, j, i)
                        os.rename(to_move[0], os.path.join(".", out_f))
                    else:
                        time.sleep(60)
                        # rename/move file
                        to_move = glob.glob(os.path.join("/home/simone/Downloads", "*.pdf"))
                        if len(to_move) > 0:
                            out_f = "{}_{}_{}.pdf".format(year_, j, i)
                            os.rename(to_move[0], os.path.join(".", out_f))
                        else:
                            pass
    # clean dir
    if len(to_delete) > 0:
        for item in to_delete:
            os.remove(item)
        else:
            pass
    # go to the next page
    to_click = driver.find_element_by_xpath(
        "/html/body/div[6]/div[6]/table[1]/tbody/tr[2]/td[3]/span/a[2]"
    )
    try:
        to_click.click()
    except:
        print("It seems this is the last page")

# %%
# That's all folks!
