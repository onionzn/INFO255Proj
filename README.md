# INFO255Proj


## Retrieve User Information from Tinder
In `get_recs.py`, we make a GET request to the Tinder endpoint `https://api.gotinder.com/v2/recs/core` to retrieve a list of users nearby.

- We need to include an `X-Auth-Token` in the header for authorization purpose. The steps to get the `X-Auth-Token` are elaborated in one of the sections below.
- Each response to the GET request returns about 45 users. We then extract the following information from each user JSON object:
    - `user_id`: The unique identifier of a Tinder user 
    - `bio`: The bio/self-intro of a Tinder user 
    - `bd`: The birthday of a Tinder user 
    - `name`: The name of a Tinder user, first Name only.
    - `gender`: The gender of a Tinder user, might be hidden.
    - `city`: The city as indicated on a Tinder user's profile
    - `distance`: A Tinder user's distance to the authenticaed user, measured in miles.
    - `company`: The company at which a Tinder user works. 
    - `job_title`: The job title of a Tinder user. 
    - `school`: The school that a Tinder user is attending or has attended.
    - `first_photo_url`: The url to the first photo on a Tinder user's profile.
- We repeat the GET request until Tinder ran out of recommendations for the authenticated user. The extracted information was written into `tinder_user.csv`. Right now, the `.csv` file contains around 4400 entries. There may be duplicates among these entries, but they can be cleaned based on the `user_id` column.
- Reference for Tinder API: https://github.com/fbessez/Tinder

#### How to execute the Python script
`python3 get_recs.py`

#### How to get `X-Auth-Token`
1. Go to this link for Tinder login with Facebook account: [Link](https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash=AeZqkIcf-NEW6vBd)
2. Before hitting the "Continue" button, open developer tools on Chrome.
3. Navigate to the "Network" tab.
4. Hit "Continue", in the "Name" sidebar 'confirm/' should appear. Click on it and click on "Response" tab.
5. Search for "access_token=" in the response.

Reference: https://github.com/charliewolf/pynder/issues/171

---
## Get Yelp Reviews using Yelp Public API

