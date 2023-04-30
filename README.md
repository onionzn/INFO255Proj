# INFO255 Final Project

## Team Members
- Kristina Hiraishi
- Jingshu Rui
- Ning Zhang

## Retrieve User Information from Tinder

### Call Tinder API
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

### Process User Information from Tinder
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
- Reference for Yelp search API: https://docs.developer.yelp.com/reference/v3_business_search
- Sample code provided by Yelp to make an API call: https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

### Step 2: Process Bussiness Information

- In `process_businesses.ipynb`, we used `pandas` and `numpy` to removed duplicates from `businesses.csv` based on the unique identifier `id`.
- The cleaned dataset is saved to `businesses_no_dup.csv`.
- In the same Jupyter notebook, we extracted a list of unique ids from `businesses.csv` and saved it to `business_ids.csv`. The list of ids will be used in the next step for id-based search of yelp reviews.


### Step 3: Retrieve Yelp Reviews by Business ID
- In `get_reviews.py`, we make Get request to the Yelp API endpoint `https://api.yelp.com/v3/businesses/{business_id_or_alias}/reviews` to retrieve reviews by business ID. For each request, we include `sort_by='yelp_sort'` as a parameter and set the `limit` to 50 (which is also the hard limit set by Yelp).
- Similar to Step 1, we need to include an `API_KEY` in the header for authorization purpose.
- Each response to the GET request returns multiple reviews, capped at. We then extract the following information from each review JSON object:
    - `review_id`: The unique identifier of a review
    - `review_url`: The url to view the review on Yelp
    - `text`: The content of the review
    - `time_created`: The time at which the review was created
    - `user_id`: The unique identifier of the author of a review
    - `user_profile_url`: The url to view the author's profile on Yelp
    - `user_image_url`: The url to view the author's profile image
    - `user_name`: The screen name of the author of a review
- The extracted information was written into `reviews.csv`. Right now, the `.csv` file contains around 12900 entries.
- Reference for Yelp reviews API: https://docs.developer.yelp.com/reference/v3_business_reviews

### Step 4: Process Yelp Reviews Dataset

- In `process_reviews.ipynb`, we used `pandas` and `numpy` to check for duplicates in `reviews.csv` based on the unique identifier `review_id`. As expected, there are no duplicates.
- In the same Jupyter notebook, we extracted first names from `user_name` and store it in a new column named `user_first_name`. This new column will be used in the next steps for cross-referencing with the Tinder user dataset.
- The processed dataset is saved to `reviews_with_first_name.csv`.

---
## Cross-match Tinder and Yelp data
### Step 1: Cross-match by first name

- In `process_cross_matching.ipynb`, we merged `reviews_with_first_name.csv` and `tinder_users_no_dup.csv` by their first name (column name `user_first_name` and `name`). 
- Since Tinder data does not have the user's last name, we were not able to check with their initials.
- Both platforms have the user's emails/phone numbers stored, but from an attacker's point of view, they do not have a public API that lets you retrieve that sensitive information.
- Worth noting, when we searched for businesses using the city as a search parameter, we implicitly used the location as a reference/quasi identifier, and the Tinder match automatically uses our current location so it’s like adding one dimension for matching accuracy.
- The merged dataset is saved to `merged.csv`.

### Step 2: Check the similarity between images
- In `process_image_matching.ipynb`, we tried to match the Yelp image (`first_photo_url`) and Tinder image (`user_image_url`) by two methods: calculating their similarity using `skimage.metrics.structural_similarity` and facial recognition methods.
- We stored the similarity score in the `image_match_ssim` and `facial_recognition` columns. 
    - image_match_ssim
        - range: [0.0037016618992177, 0.7184725111995259]
        - > 0.7: 3/14888 = 0.0002015045674368619
        - > 0.65: 21/14888 = 0.0014105319720580333
        - > 0.6: 97/14888 = 0.006515314347125201
        - > 0.55: 323/14888 = 0.021695325094035465
        - > 0.5: 807/14888 = 0.05420472864051585
    - facial_recognition
        - the algorithm failed to detect faces.
        - Probably because most of the photos are group photos, and a lot of them are wearing masks.
- However by clicking into some links with relatively high similarity scores, they still might not be the same person. We think it's reasonale people tend to put different pictures on their Tinder than their social media profile picture.
- The processed dataset is saved into `image_similarity.csv`.

### Step 3: Explore 3rd party authentication
- We want to explore if the 3rd party authorization, such as using Facebook account to log in to both Yelp and Tinder applications, would help improve the cross-matching between the two platforms.
- According to our research, the short answer is no (OAuth provides a decent level of privacy)
    - Most third-party websites (that require you to have an account) understand the reluctance of users to create new accounts. In order to ensure that they do not lose out on such ‘reluctant’ users, these third-party websites implement the OAuth standard in their system.
    - OAuth is a protocol that allows third-party websites to access and retrieve select pieces of their users’ information in order to authenticate users. 
    - Most of the time when electing to use social login, the third-party website or app lets us know what information they are requesting access to. They use an access token provided by the authentication provider to gain **restricted/limited** access to some of your account information.
    - When it comes to the data that Facebook in particular has about each of its users and what it allows third-party apps to have access to, the social media giant has a strict Platform Policy that outlines what developers of third-party apps can and cannot do. With regards to data, third-party apps are required to “provide a publicly available and easily accessible privacy policy that *explains what data you are collecting and how you will use that data*.”
    - source: https://medium.com/@golman.alan/social-login-3rd-party-app-authorization-f228a3f8ae23
- Yelp privacy terms for third-party integrations:
    - Third-Party Integrations: If you sign up for, or log into, Yelp using a third-party service like Facebook or Google, or link your Yelp account to your account with a third-party service like Facebook, Instagram, or Twitter, we may receive information about you from such third party service. If you post content to a third-party service through the Service, that third-party service will also receive that content, which will be visible to anyone that has access to it through that third-party service. Some of our web pages utilize framing techniques to serve content to you from our third-party partners while preserving the look and feel of the Service. In such cases, please note that the information you provide may be transmitted directly to the identified third-party partner. If you interact with businesses through Yelp, they will receive whatever information you choose to share with them, for example, the contact information you share through direct messages to the business or your phone number if you call the business.
    - source: https://terms.yelp.com/privacy/en_us/20200101_en_us/#third-parties
    - pretty vague
- Tinder privacy terms
    - Information We Collect
        It goes without saying, we can’t help you develop meaningful connections without some information about you, such as basic profile details and the types of people you’d like to meet. We also collect information about your use of our services such as access logs, as well as information from third parties, like when you access our services through your social media account or when you upload information from your social media account to complete your profile. If you want additional info, we go into more detail below.
    - source: https://policies.tinder.com/privacy/us/en
- Neither Yelp nor Tinder stores the user's Facebook or Google account information directly on its platform. They do not have access to the user's password or any other sensitive information associated with their Facebook or Google account. So 3rd party auth does not provide additional information that results in linking / data fusion.