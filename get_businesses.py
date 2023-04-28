from pandas import *
from urllib.parse import quote
import requests, json, csv

from YELP_API_KEY import YELP_API_KEY

API_KEY = YELP_API_KEY

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_LIMIT = 50

FIELD_NAMES = ['id', 'name', 'price', 'city', 'state', 'zip_code']

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...{1}'.format(url, url_params.get('location')))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return json.loads(response.content)

def search(api_key,location, term=""):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params).get('businesses')

def make_dict_list(businesses):
    business_info_list = []
    if businesses is None:
        return business_info_list

    for business in businesses:
        business_info = dict()
        business_info['id'] = business.get('id')
        business_info['name'] = business.get('name')
        business_info['price'] = business.get('price')
        business_info['city'] = business.get('location').get('city')
        business_info['state'] = business.get('location').get('state')
        business_info['zip_code'] = business.get('location').get('zip_code')
        business_info_list.append(business_info)
    return business_info_list

def load_cities():
    cities_df = read_csv("./data/cities.csv")
    cities = cities_df.iloc[:, 0].tolist()
    return cities

def write_header_to_csv():
    with open('./data/businesses.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = FIELD_NAMES)
        writer.writeheader()
    csvfile.close()

def main():
    cities = load_cities()
    with open('./data/businesses.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        for city in cities:
            businesses = search(API_KEY, city)
            dict_list = make_dict_list(businesses)
            for dictionary in dict_list:
                writer.writerow(dictionary)        
    csvfile.close()


if __name__ == "__main__":
    main()
    