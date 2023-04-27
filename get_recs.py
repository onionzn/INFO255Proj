import requests, json, csv

API_BASE = 'https://api.gotinder.com'
X_AUTH_TOKEN = "placeholder"

LAT_BERK = -122.272743
LON_BERK = 37.871593

LAT_SF = 37.773972
LON_SF = -122.431297

LAT_NYC = 40.776676
LON_NYC = -73.971321

def get_recs():
    content = json.loads(requests.get(API_BASE + "/v2/recs/core", headers={"X-Auth-Token": X_AUTH_TOKEN}).content)
    users = content["data"]["results"]
    return users

def change_location(lat, lon):
    location = {"lat": lat, "lon": lon}
    res = requests.post(API_BASE + "/user/ping", headers={"X-Auth-Token": X_AUTH_TOKEN}, json=location)
    print("response to change location post request:")
    print(res.status_code)
    print(res.reason)

def make_dict_list(rec_users):
    
    dict_list = []

    for user in rec_users:
        dictionary = dict()

        user_info = user.get('user')

        # basic demographic information
        user_id = user_info.get('_id')
        bio = user_info.get('bio')
        bd = user_info.get('birth_date')
        name = user_info.get('name')
        dictionary['user_id'] = user_id
        dictionary['bio'] = bio
        dictionary['bd'] = bd
        dictionary['name'] = name
        print(name)

        # gender
        gender = user_info.get('gender')
        if gender == 1:
            gender = 'female'
        elif gender == 0:
            gender = 'male'
        else:
            gender = 'not displayed'
        print("gender: " + gender)
        dictionary['gender'] = gender

        # city
        city = ''
        if user_info.get('city') is not None:
            city = user_info.get('city').get('name')
        print("city: " + city)
        dictionary['city'] = city

        # distance from user in miles
        distance = user.get('distance_mi')
        dictionary['distance'] = distance

        # first job
        company = ''
        job_title = ''
        jobs = user_info.get('jobs')
        if jobs is not None and len(jobs) > 0:
            first_job = jobs[0]
            if first_job.get('company') is not None:
                company = first_job.get('company').get('name')
            if first_job.get('title') is not None:
                job_title = first_job.get('title').get('name')
        print("company: " + company)
        print("job_title: " + job_title)
        dictionary['company'] = company
        dictionary['job_title'] = job_title

        # first school
        school = ''
        schools = user_info.get('schools')
        if schools is not None and len(schools) > 0:
            school = schools[0].get('name')
        print("school: " + school)
        dictionary['school'] = school

        # url of the first photo
        first_photo_url = ''
        photos = user_info['photos']
        first_photo_url = photos[0]['url']
        dictionary['first_photo_url'] = first_photo_url
        print("----------------------------")

        dict_list.append(dictionary)

    return dict_list


def main():
    # change the geographic location of user
    change_location(LAT_BERK, LON_BERK)
    
    # retrieve a list of users
    rec_users = get_recs()
    dict_list = make_dict_list(rec_users)
    field_names = ['user_id', 'bio', 'bd', 'name', 'gender', 'city', 'distance', 'company', 'job_title', 'school', 'first_photo_url']

    
    with open('tinder_users.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        #writer.writeheader()
        for dictionary in dict_list:
            writer.writerow(dictionary)
            
    csvfile.close()


if __name__ == "__main__":
    for i in range(10):
        main()
