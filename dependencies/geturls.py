from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from time import sleep
import json
import sys
import os

class ScraperUrls():

    def __init__(self,DRIVER_PATH,LOG_FOLDER):
        self.DRIVER_PATH = DRIVER_PATH
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1920,1200")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.options, executable_path=DRIVER_PATH)

    def GoToPage(self,page):
        self.driver.get(page)

    def GetListingQuantity(self):
        ListingQuantity = self.driver.find_element_by_xpath("/html/body/div[@id='__next']/div[@class='UtilityProvider-wqw4uj-0 gDcynq']/div[@class='appprovider__AppThemeWrapper-asxde5-0 gWkYZE']/div[@class='Layout__LayoutStyled-sc-9y7jis-0 ibZBWk page-container']/div[@class='Container-u38a83-0 jDuhNh inner-container container']/div[@class='Row-sc-2hg243-0 iUVxfs align-items-center mb-4 row']/div[@class='Col-sc-14ninbu-0 lfGZKA mb-3 mb-sm-0 col-12 col-md-8']/span[@class='Breadcrumb-sc-15mocrt-0 aAjZo Breadcrumb-sc-1df07y0-0 bLMdQH valing-center d-block breadcrumb']/h1[@class='H1-xsrgru-0 jdfXCo d-sm-inline-block breadcrumb-item active']")

        return int(ListingQuantity.text.split(" ")[0])

    def GetUrls(self):
        urls = self.driver.find_elements_by_xpath("//a[@class='sc-bdVaJa ebNrSm']")

        url_list = []

        for url in urls:
            url_list.append(url.get_attribute("href"))

        for url in url_list:
            if url == None:
                url_list.remove(url)

        return url_list

    def NextPage(self):
        NextPageButton = self.driver.find_element_by_xpath("/html/body/div[@id='__next']/div[@class='UtilityProvider-wqw4uj-0 gDcynq']/div[@class='appprovider__AppThemeWrapper-asxde5-0 gWkYZE']/div[@class='Layout__LayoutStyled-sc-9y7jis-0 ibZBWk page-container']/div[@class='Container-u38a83-0 jDuhNh inner-container container']/div[@class='Row-sc-2hg243-0 iUVxfs row']/div[@class='Col-sc-14ninbu-0 lfGZKA col-md-8 col-lg-9']/ul[@class='sc-dVhcbM kVlaFh Pagination-w2fdu0-0 cxBThU paginator justify-content-center align-items-baseline pagination']/li[@class='item-icon-next page-item']/a[@class='sc-bdVaJa ebNrSm page-link']")
        #webdriver.ActionChains(self.driver).move_to_element(NextPageButton).click(NextPageButton).perform()
        webdriver.ActionChains(self.driver).move_to_element(NextPageButton)
        NextPageButton.click()

    def AcceptCookies(self):
        OkBtn = self.driver.find_element_by_xpath("//a[@class='sc-bdVaJa ebNrSm sc-htoDjs brhAsq Button-bepvgg-0 dqiWxy text-center btn-disclaimer btn btn-secondary']")
        #webdriver.ActionChains(self.driver).move_to_element(NextPageButton).click(NextPageButton).perform()
        OkBtn.click()

    def Stop(self):

        self.driver.quit()
