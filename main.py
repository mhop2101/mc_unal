from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ConnectionError
from json.decoder import JSONDecodeError

from dependencies.getdetails import ScrapeDetails
from dependencies.geturls import ScraperUrls
from dependencies.clean import UrlCleaner

from time import sleep
import platform
import json
import sys
import os

WEBDRIVER_DELAY_EXTENDED = 10
WEBDRIVER_DELAY = 5
currentdir = os.path.dirname(os.path.realpath(__file__))
LOG_FOLDER = os.path.join(currentdir,'logs')

if platform.system() == 'Windows':
    DRIVER_PATH = os.path.join(currentdir,'ChromeDriverWin','chromedriver.exe')
else:
    DRIVER_PATH = os.path.join(currentdir,'ChromeDriverMac','chromedriver')

FRAME = os.path.join(currentdir,'logs','frame.csv')
HEADERS = [
           {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'},
           {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}]

if __name__ == '__main__':

    try:
        sys.argv[1]
    except IndexError:
        print('\nNo parameter given\n')
        print('Please specify a parameter from the ones listed below\n')
        print('- get [URL]')
        print('- clean')
        print('- scrape [true/false]\n')
        print('Usage: python main.py [parameter] [details]\n')
        exit()

    if sys.argv[1] == 'get':
        url = sys.argv[2]

        # Initialize the scraper class with the path to chromedriver.exe as a parameter
        scraper = ScraperUrls(DRIVER_PATH,LOG_FOLDER)

        # Go to the url in the parameter
        scraper.GoToPage(str(url))

        sleep(WEBDRIVER_DELAY_EXTENDED)

        # Get the amount of pages that have to be iterated through
        # Lisitng quantity / Total number of listings
        listings = scraper.GetListingQuantity()
        numpages = listings / 50

        #Set dictionary to store all urls
        data = {}
        data['listing'] = []

        #Accept terms of cookie use
        scraper.AcceptCookies();

        # For every page
        for i in range(int(numpages)):

            sleep(WEBDRIVER_DELAY)

            # Get the listing urls in the current page
            urls = scraper.GetUrls()

            # Append every url in the list to the dictionary
            for url in urls:
                data['listing'].append({
                'url':url,
                'scraped':'False'
                })

            # write the data to a json file
            with open(os.path.join(LOG_FOLDER,'urls.json'), 'w') as outfile:
                json.dump(data, outfile,indent=4)

            # Go to the next page
            try:
                scraper.NextPage()
                print(i,'\n\n')
            except NoSuchElementException:
                print("exiting")
                exit()
                #break

            sleep(WEBDRIVER_DELAY)

        # quit selenium's webdriver instance
        scraper.Stop()

    if sys.argv[1] == 'clean':
        cleaner = UrlCleaner(LOG_FOLDER)
        cleaner.Clean()
        cleaner.ExportData()

    if sys.argv[1] == 'scrape':

        if sys.argv[2] == 'true':
            GEOCODING = True
        else:
            GEOCODING = False

        try:
            scraper = ScrapeDetails(LOG_FOLDER,HEADERS,FRAME,GEOCODING)

            with open(os.path.join(LOG_FOLDER,'urls_cleaned.json'), 'r') as infile:
                array = json.load(infile)

            for i in array:
                if i['scraped'] == 'False':
                    try:
                        scraper.GetDetails(i['url'])
                        i['scraped'] = 'True'
                        with open(os.path.join(LOG_FOLDER,'urls_cleaned.json'), 'w') as outfile:
                            json.dump(array, outfile,indent=4)
                    except ConnectionError:
                        print('Resource blocked, change your internet protocol or try again later')
                        exit()
            print('Done!')
        except KeyboardInterrupt:
            print('\nPaused, run the script again to resume')
        except JSONDecodeError:
            print('The file urls_cleaned.json appears to have a problem')
