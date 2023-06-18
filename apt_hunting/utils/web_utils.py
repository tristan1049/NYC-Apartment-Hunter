import yaml

# REQUESTS CONSTANTS
STREETEASY_URL = "https://streeteasy.com/for-rent/nyc/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

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

# YAML CONSTANTS
CONFIRM_LIST = ['yes', 'y']
BATHS_LIST = [1, 1.5, 2, 2.5, 3, 3.5, 4]

def get_filters():
    # TODO: Make this compatible with calling program from not root directory
    # TODO: Check if this file exists first as well
    with open('filters.yaml', 'r') as file:
        return yaml.safe_load(file) 
   
def validate_baths(baths):
    if baths:
        if baths not in BATHS_LIST:
            if baths < 1:
                baths = 1
            elif baths > 4:
                baths = 4
            baths = round(baths)
    return baths

def validate_beds(min_beds, max_beds):
    if min_beds:
        if min_beds < 0:
            min_beds = 0
        elif min_beds > 4:
            min_beds = 4
    if max_beds:
        if max_beds < 0:
            max_beds = 0
        elif max_beds > 4:
            max_beds = 4
    if min_beds and max_beds:
        if min_beds > max_beds:
            max_beds = min_beds 
    return min_beds, max_beds

def get_streeteasy_url_with_filters(page_num=1):
    url = STREETEASY_URL
    filters = get_filters()

    # Add price tag to url
    min_price = '' if filters['price']['min'] == None else filters['price']['min']
    max_price = '' if filters['price']['max'] == None else filters['price']['max'] 
    url += 'price:{}-{}%7C'.format(min_price, max_price)

    # Add area tags to url
    areas = []
    if filters['boroughs']['Manhattan'] != None:
        areas = [MANHATTAN_CODE] if (filters['boroughs']['Manhattan'].strip().lower()) in CONFIRM_LIST else []
    if filters['boroughs']['Bronx'] != None:
        areas = areas + [BRONX_CODE] if filters['boroughs']['Bronx'].strip().lower() in CONFIRM_LIST else []
    if filters['boroughs']['Brooklyn'] != None:
        areas = areas + [BROOKLYN_CODE] if filters['boroughs']['Brooklyn'].strip().lower() in CONFIRM_LIST else []
    if filters['boroughs']['Queens'] != None:
        areas = areas + [QUEENS_CODE] if filters['boroughs']['Queens'].strip().lower() in CONFIRM_LIST else []
    if filters['boroughs']['North Jersey'] != None: 
        areas = areas + [NORTH_JERSEY_CODE] if filters['boroughs']['North Jersey'].strip().lower() in CONFIRM_LIST else []
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

    # Add move in date
    if filters['move_in']['before'] != None:
        url += 'available:{}%7C'.format(filters['move_in']['before'])
    elif filters['move_in']['after'] != None:
        url += 'available_after:{}%7C'.format(filters['move_in']['after'])

    return url