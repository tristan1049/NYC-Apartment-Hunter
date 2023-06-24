import json
import urllib
from datetime import datetime

from utils.filters_utils import get_filters
from utils.filters_utils import is_valid_filter
from utils.filters_utils import validate_baths
from utils.filters_utils import validate_beds
from utils.filters_utils import CONFIRM_LIST

# REQUESTS CONSTANTS
STREETEASY_URL = "https://streeteasy.com/for-rent/nyc/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
API_FILE = 'api.json'
NEW_YORK_SUFFIX = 'New York NY'
COMMUTE_LIMIT_EXCEEDED = 'Commute limit exceeded'

# HTML CONSTANTS
LISTING_CLASS = 'searchCardList--listItem'
BUILDING_CLASS = 'listingCardLabel listingCardLabel-grey listingCard-upperShortLabel'
PRICE_CLASS = 'price listingCard-priceMargin'
BEDS_CLASS = 'listingDetailDefinitionsIcon listingDetailDefinitionsIcon--bed'
BATHS_CLASS = 'listingDetailDefinitionsIcon listingDetailDefinitionsIcon--bath'
SQ_FT_CLASS = 'listingDetailDefinitionsIcon listingDetailDefinitionsIcon--measure'

# BOROUGH AREA CODES CONSTANTS
MANHATTAN_CODE = '100'
BRONX_CODE = '200'
BROOKLYN_CODE = '300'
QUEENS_CODE ='400'
NORTH_JERSEY_CODE = '800000'  # StreetEasy is so weird for this

def get_streeteasy_url_with_filters(page_num=1):
    url = STREETEASY_URL
    filters = get_filters()

    # Add price tag to url
    min_price = '' if filters['price']['min'] == None else filters['price']['min']
    max_price = '' if filters['price']['max'] == None else filters['price']['max'] 
    url += 'price:{}-{}%7C'.format(min_price, max_price)

    # Add area tags to url
    areas = []
    areas += [MANHATTAN_CODE] if is_valid_filter(filters['boroughs']['Manhattan']) else []
    areas += [BRONX_CODE] if is_valid_filter(filters['boroughs']['Bronx']) else []
    areas += [BROOKLYN_CODE] if is_valid_filter(filters['boroughs']['Brooklyn']) else []
    areas += [QUEENS_CODE] if is_valid_filter(filters['boroughs']['Queens']) else []
    areas += [NORTH_JERSEY_CODE] if is_valid_filter(filters['boroughs']['North Jersey']) else []
    url += 'area:{}%7C'.format(','.join(areas))

    # Add bath tag to url
    baths = validate_baths(filters['baths']['min'])
    if baths != None:
        url += 'baths>={}%7C'.format(baths)

    # Add beds tag to url
    beds = ''
    min_beds = filters['bedrooms']['min']
    max_beds = filters['bedrooms']['max']
    min_beds, max_beds = validate_beds(filters['bedrooms']['min'], filters['bedrooms']['max'])
    if min_beds == None and max_beds != None:
        beds = '<={}'.format(max_beds)
    elif min_beds != None and max_beds == None: 
        beds = '>={}'.format(min_beds)
    elif min_beds != None and max_beds != None:
        beds = ':{}-{}'.format(min_beds, max_beds)
    url += 'beds{}%7C'.format(beds)

    # Add laundry and pets tags to url (grouped as amenities)
    amenities_dict = {'washer_dryer':filters['laundry']['in_unit'], 
                      'laundry':filters['laundry']['in_building'], 
                      'pets':filters['pets']}
    amenities = [amenity for amenity in amenities_dict if amenities_dict[amenity] in CONFIRM_LIST]
    if len(amenities) > 0:
        url += 'amenities:{}%7C'.format(','.join(amenities))

    # Add move in date to url
    if filters['move_in']['before'] != None:
        url += 'available:{}%7C'.format(filters['move_in']['before'])
    elif filters['move_in']['after'] != None:
        url += 'available_after:{}%7C'.format(filters['move_in']['after'])

    # Add page number to url
    url += '?page={}'.format(page_num)

    return url

def get_commute_time_url(address, address_suffix=None):
    filters = get_filters()
    dest = filters['commute']['address']
    mode = filters['commute']['mode_transportation']
    time_limit = filters['commute']['time_limit']
    year = filters['commute']['year']
    month = filters['commute']['month']
    day = filters['commute']['day']
    hour = filters['commute']['hour']
    minute = filters['commute']['minute']

    if dest == None or time_limit == None:
        return None
    if address_suffix != None:
        address += ' ' + address_suffix
    # Set commute_time in Epoch standard for API
    if None in [year, month, day, hour]:
        commute_time = datetime.now().strftime('%s')
    elif minute == None:
        commute_time = datetime(year, month, day, hour).strftime('%s')
    else:
        commute_time = datetime(year, month, day, hour, minute).strftime('%s')
    
    with open(API_FILE, 'r') as file:
        api_key = json.load(file)
        api_key = api_key['apikey']

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    url += '?origins={}'.format(urllib.parse.quote(address))
    url += '&destinations={}'.format(urllib.parse.quote(dest))
    url += '&departure_time={}'.format(urllib.parse.quote(str(commute_time)))
    url += '&mode={}'.format(urllib.parse.quote(mode))
    url += '&key={}'.format(api_key)

    return url
