from pandas import *
from urllib.parse import quote
import requests, json, csv
from YELP_API_KEY import YELP_API_KEY

API_KEY = YELP_API_KEY
API_HOST = 'https://api.yelp.com'
REVIEW_PATH = '/v3/businesses/{0}/reviews'
LIMIT = 50
SORT_BY = 'yelp_sort'
FIELD_NAMES = ['review_id', 'review_url', 'text', 'time_created', 'user_id', 'user_profile_url', 'user_image_url', 'user_name']


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return json.loads(response.content)

def get_reviews(api_key, business_id):
    url_params = {
        'limit': LIMIT,
        'sort_by': SORT_BY
    }

    review_path_complete = REVIEW_PATH.format(business_id)
    return request(API_HOST, review_path_complete, api_key, url_params=url_params).get('reviews')

def load_business_ids():
    business_ids_df = read_csv("./data/businesses_ids.csv")
    business_ids = business_ids_df.iloc[:, 0].tolist()
    return business_ids

def write_header_to_csv():
    with open('./data/reviews.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = FIELD_NAMES)
        writer.writeheader()
    csvfile.close()

def make_dict_list(reviews):
    review_info_list = []
    if reviews is None:
        return review_info_list

    for review in reviews:
        review_info = dict()
        review_info['review_id'] = review.get('id')
        review_info['review_url'] = review.get('url')
        review_info['text'] = review.get('text')
        review_info['time_created'] = review.get('time_created')
        review_info['user_id'] = review.get('user').get('id')
        review_info['user_profile_url'] = review.get('user').get('profile_url')
        review_info['user_image_url'] = review.get('user').get('image_url')
        review_info['user_name'] = review.get('user').get('name')

        review_info_list.append(review_info)
    return review_info_list

def main():
    business_ids = load_business_ids()
    with open('./data/reviews.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        for business_id in business_ids:
            reviews = get_reviews(API_KEY, business_id)
            dict_list = make_dict_list(reviews)
            for dictionary in dict_list:
                writer.writerow(dictionary)        
    csvfile.close()

if __name__ == "__main__":
    main()