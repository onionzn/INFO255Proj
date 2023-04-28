# INFO255 Final Project

## Team Members
- Kristina Hiraishi
- Jingshu Rui
- Ning Zhang

## Retrieve User Information from Tinder
In `get_recs.py`, we make a GET request to the Tinder endpoint `https://api.gotinder.com/v2/recs/core` to retrieve a list of users nearby.

- We need to include an `X-Auth-Token` in the header for authorization purpose. The steps to get the `X-Auth-Token` are elaborated in one of the sections below.
- Each response to the GET request returns about 45 users. We then extract the following information from each user JSON object:
    - `user_id`: The unique identifier of a Tinder user 
    - `bio`: The bio/self-intro of a Tinder user 
    - `bd`: The birthday of a Tinder user 
    - `name`: The name of a Tinder user, first Name only
    - `gender`: The gender of a Tinder user, might be hidden
    - `city`: The city as indicated on a Tinder user's profile
    - `distance`: A Tinder user's distance to the authenticaed user, measured in miles
    - `company`: The company at which a Tinder user works
    - `job_title`: The job title of a Tinder user
    - `school`: The school that a Tinder user is attending or has attended
    - `first_photo_url`: The url to the first photo on a Tinder user's profile
- We repeat the GET request until Tinder ran out of recommendations for the authenticated user. The extracted information was written into `tinder_user.csv`. Right now, the `.csv` file contains around 4400 entries. There may be duplicates among these entries, but they can be cleaned based on the `user_id` column.
- Reference for Tinder API: https://github.com/fbessez/Tinder

#### How to execute the Python script
`python3 get_recs.py`

#### How to get `X-Auth-Token`
1. Log into your Tinder account.
2. Open Developer Tool on Chrome.
3. From console do follow command: `localStorage.getItem('TinderWeb/APIToken')`

Reference: https://github.com/ChristopherProject/TinderHack2023

## Process User Information from Tinder
- In `process_tinder_users.ipynb`, we used `pandas` and `numpy` to removed duplicates from `tinder_users.csv` based on the unique identifier `user_id`.
- The cleaned dataset is saved to `tinder_users_no_dup.csv`.
- In the same Jupyter notebook, we extracted a list of unique cities from `tinder_users.csv` and saved it to `cities.csv`. The list of cities will be used in the next step for location-based search of businesses using Yelp API.

---
## Get Yelp Reviews Using Yelp Public API

### Step 1: Get Bussiness Information Based on Cities

- In `get_businesses.py`, we make GET requests to the Yelp API endpoint `https://api.yelp.com/v3/businesses/search` to search for businesses. For each request, we include a city name as a search parameter and set the search limit to 50 (which is also the hard limit set by Yelp).

- We need to include an `API_KEY` in the header for authorization purpose. The steps to get the `API_KEY` are elaborated in this YELP documentation: https://docs.developer.yelp.com/docs/fusion-authentication
- Each response to the GET request returns about 50 businesses. We then extract the following information from each business JSON object:
    - `id`: The unique identifier of a business 
    - `name`: The name of a business
    - `price`: The price level of a business, represented by the number of dollar signs
    - `city`: The city where a business is located
    - `state`: The state where a business is located
    - `zip_code`: The zipcode of a business
- The extracted information was written into `businesses.csv`. Right now, the `.csv` file contains around 4900 entries. There may be duplicates among these entries, but they can be cleaned based on the `id` column.
- Reference for YELP search API: https://docs.developer.yelp.com/reference/v3_business_search
- Sample code provided by YELP to make an API call: https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py
