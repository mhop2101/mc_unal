from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from time import sleep
import secrets
import pickle
import json
import sys
import os

class ScraperUrls():

    def __init__(self,DRIVER_PATH,LOG_FOLDER):
        self.LOG_FOLDER = LOG_FOLDER
        self.DRIVER_PATH = DRIVER_PATH
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1720,1000")
        self.options.add_argument('--ignore-ssl-errors=yes')
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--user-data-dir={}".format(os.path.join(LOG_FOLDER,'USER_DATA')))
        self.driver = webdriver.Chrome(options=self.options, executable_path=DRIVER_PATH)

    def AddCookies(self):
        # GET COOKIES
        '''
        pickle.dump( self.driver.get_cookies() , open(os.path.join(self.LOG_FOLDER,"cookies.pkl"),"wb"))
        print(self.driver.get_cookies())
        cookies = pickle.load(open(os.path.join(self.LOG_FOLDER,"cookies.pkl"), "rb"))
        for cookie in cookies:
            #self.driver.add_cookie(cookie)
            print(cookie)
        print('Cookies added !')
        '''
        '''
        self.driver.get('https://www.metrocuadrado.com/cas/login?service=https%3A%2F%2Fwww.metrocuadrado.com%2Fmetrocuadrado-personal-account%2Flogin%2Fcas')
        print(self.driver.manage().getCookies())
        self.driver.find_element_by_id("registerNewUser").click()
        sleep(2)
        self.driver.find_element_by_id("newUserEmail").send_keys(secrets.token_hex(16) + '@yopmail.com')
        sleep(2)
        self.driver.find_element_by_class_name("checkReq").click()
        sleep(2)
        self.driver.find_element_by_id("btnCreateAccount").click()
        sleep(2)
        self.driver.find_element_by_id("acceptEmailSentBtn").click()
        sleep(50)
        '''

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
        #Footer = self.driver.find_element_by_xpath("/html/body/div[@id='__next']/div[@class='UtilityProvider-wqw4uj-0 gDcynq']/div[@class='appprovider__AppThemeWrapper-asxde5-0 gWkYZE']/div[@class='Layout__LayoutStyled-sc-9y7jis-0 ibZBWk page-container']/div[@class='Container-u38a83-0 jDuhNh inner-container container']/section[@class='Prefooter-sc-9b263-0 igRJXo']/div[@class='Row-sc-2hg243-0 iUVxfs row']/div[@class='Col-sc-14ninbu-0 lfGZKA text-left text-lg-center col-lg-12']")
        NextPageButton = self.driver.find_element_by_xpath("/html/body/div[@id='__next']/div[@class='UtilityProvider-wqw4uj-0 gDcynq']/div[@class='appprovider__AppThemeWrapper-asxde5-0 gWkYZE']/div[@class='Layout__LayoutStyled-sc-9y7jis-0 ibZBWk page-container']/div[@class='Container-u38a83-0 jDuhNh inner-container container']/div[@class='Row-sc-2hg243-0 iUVxfs row']/div[@class='Col-sc-14ninbu-0 lfGZKA col-md-8 col-lg-9']/ul[@class='sc-dVhcbM kVlaFh Pagination-w2fdu0-0 cxBThU paginator justify-content-center align-items-baseline pagination']/li[@class='item-icon-next page-item']/a[@class='sc-bdVaJa ebNrSm page-link']")
        #NextPageButton = self.driver.find_element_by_class_name("sc-bdVaJa ebNrSm page-link")
        webdriver.ActionChains(self.driver).move_to_element(NextPageButton).click(NextPageButton).perform()
        #webdriver.ActionChains(self.driver).move_to_element(Footer)
        #sleep(2)
        NextPageButton.click()

    def AcceptCookies(self):
        try:
            OkBtn = self.driver.find_element_by_xpath("//a[@class='sc-bdVaJa ebNrSm sc-htoDjs brhAsq Button-bepvgg-0 dqiWxy text-center btn-disclaimer btn btn-secondary']")
            #webdriver.ActionChains(self.driver).move_to_element(NextPageButton).click(NextPageButton).perform()
            OkBtn.click()
        except:
            pass


    def Stop(self):

        self.driver.quit()
