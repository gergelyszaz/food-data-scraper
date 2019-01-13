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

    # Parse properties
    for prop in site['properties'].split('|'):
        xpath = site['{}.xpath'.format(prop)]
        regex = site['{}.regex'.format(prop)]
        
        propValue =  [
            v.group(1) if v else None for v in
            [re.search(regex, info.text) if info.text else '' for info in tree.xpath(xpath)]
        ][0]
        if(propValue) :
            data[prop] = propValue 
        else :
            print('Value for {} not found'.format(prop))
    
    return data


def populateDataSet(site):
    foods = []
    ###### Scrape data
    print('Scraping ' + site['url'])
    for date in site['date'].split('|'):
        print('Getting data for {}'.format(date))
        for category in site['category'].split('|'):
            print(category)
            url = site['food.url'].format(category=category,date=date)
            print(url)
            data = getFoodData(site, url)
            if(data) :
                foods.append(data)

    return foods

if __name__ == "__main__":
    import sys
    import configparser
    
    config = configparser.ConfigParser()
    config.read('config.INI', 'UTF-8')
    site = config[sys.argv[1]]
    site['date'] = sys.argv[2]

    data = populateDataSet(site)

    print(data)