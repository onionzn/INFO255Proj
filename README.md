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
- We repeat the GET request until Tinder ran out of recommendations for the authenticated user. The extracted information was written into a `tinder_user.csv`.

#### How to execute the Python script
`python3 get_recs.py`

#### How to get `X-Auth-Token`
