import json
import os

class UrlCleaner():

    def __init__(self,LOG_FOLDER):
        # Define local log folder
        self.LOG_FOLDER = LOG_FOLDER

        # Open json file to clean
        with open(os.path.join(self.LOG_FOLDER,'urls.json'), 'r') as infile:
            self.array = json.load(infile)

    def Clean(self):
        # Get the lisitngs dictionary
        data = self.array['listing']

        # set results list
        self.result = list()

        # set seen items set
        items_set = set()

        items_set.add('https://www.metrocuadrado.com/')
        items_set.add('https://www.metrocuadrado.com/apartamentos/')
        items_set.add('https://www.metrocuadrado.com/apartamentos/venta/')
        items_set.add('https://www.metrocuadrado.com/apartamentos/venta/bogota/')


        # data cleaning
        for item in data:
            # only add unseen items (referring to 'title' as key)
            if not item['url'] in items_set:
                # mark as seen
                items_set.add(item['url'])
                # add to results
                self.result.append(item)

    def ExportData(self):
        # Export results to json file with same structure
        with open(os.path.join(self.LOG_FOLDER,'urls_cleaned.json'), 'w') as outfile:
           json.dump(self.result, outfile,indent=4)
