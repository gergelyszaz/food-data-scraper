import requests
import re
from lxml import html

# returns nil if url is not available
def getFoodData(site, url):
    data = {}
    page = requests.get(url)

    if page.status_code != 200 or not page.text:
        return None
    tree = html.fromstring(page.text)

    # Parse values
    data['name'] = tree.xpath(site['food.xpath'])[0]
    print(data['name'])
    data['category'] = data['name'].split(' ', 1)[0]
    print(data['category'])

    # Parse properties
    for prop in site['properties'].split('|'):
        print(prop)
        xpath = site['{}.xpath'.format(prop)]
        regex = site['{}.regex'.format(prop)]
        
        data[prop] = [
            v.group(1) if v else -9999 for v in
            [re.search(regex, info.text) if info.text else '' for info in tree.xpath(xpath)]
        ][0]

        print(data[prop])
    
    return data


def populateDataSet(site):

    ###### Scrape data
    print('Scraping ' + site['url'])
    for date in site['date'].split('|'):
        print('Getting data for {}'.format(date))
        for category in site['category'].split('|'):
            print(category)
            url = site['food.url'].format(category=category,date=date)
            print(url)
            data = getFoodData(site, url)

    return data

if __name__ == "__main__":
    import sys
    import configparser
    
    config = configparser.ConfigParser()
    config.read('config.INI', 'UTF-8')
    site = config[sys.argv[1]]

    data = populateDataSet(site)

    print(data)