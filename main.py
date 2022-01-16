# Business Search https://api.yelp.com/v3/businesses/search
# Detailed Business Content https://api.yelp.com/v3/businesses/{id}

# import the modules
import random
import requests  # module used to request from API
from YelpAPI import get_my_key

# Define number of recommendations
NUM_RECOMMENDATIONS = 20
# Define the API Key
API_KEY = get_my_key()
# Define the Endpoint
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'  # where we are making requests from
# Define Header (info or metadata that we send when we make our request, authenticates ourselves)
HEADERS = {'Authorization': 'bearer %s' % API_KEY}
# Define parameters
PARAMETERS = {'term': 'restaurants',
              'limit': 50,
              'radius': 24140,
              'offset': 0,
              'location': 'Santa Cruz'}
# Make a request to the yelp API
response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
# convert the JSON string to a Dictionary
business_data = response.json()

# prints every business in the area
# for business in recommended_businesses:
#     print(business)

all_businesses = []
while len(all_businesses) < business_data['total']:
    for business in business_data['businesses']:
        new_business = (business['name'], business['id'])
        all_businesses.append(new_business)
    PARAMETERS['offset'] += 50
    # Make a request to the yelp API
    response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    # convert the JSON string to a Dictionary
    business_data = response.json()

business_set = set(all_businesses)
list_recommendations = random.sample(business_set, NUM_RECOMMENDATIONS)

# for rec in list_recommendations:
#     print(rec)
# create a dictionary for each business with keys for
# - reviews
# - amount of reviews
# - distance
# - pictures
# - restaurant name
# - category of food
# - price

biz_list = []
for rec in list_recommendations:
    biz = {'name': '', 'category': [], 'price': '', 'rating': 0, 'num_reviews': 0, 'address': '', 'pictures': []}
    biz_id = rec[1]
    # print(rec[0])
    # print(biz_id)
    ENDPOINT = 'https://api.yelp.com/v3/businesses/{}'.format(biz_id)
    PARAMETERS = {}
    response = requests.get(url=ENDPOINT, params=PARAMETERS, headers=HEADERS)
    # convert the JSON string to a Dictionary
    business_data = response.json()
    biz['name'] = business_data['name']
    for category in business_data['categories']:
        biz['category'].append(category['title'])
    if 'price' in business_data:
        biz['price'] = business_data['price']
    biz['rating'] = business_data['rating']
    biz['num_reviews'] = business_data['review_count']
    biz['address'] = business_data['location']['display_address']
    biz['pictures'] = business_data['photos']
    biz_list.append(biz)

print(biz_list)
