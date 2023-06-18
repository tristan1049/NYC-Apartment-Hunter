from datetime import date

from utils.filters_utils import get_filters
from utils.filters_utils import is_valid_filter

# DB METADATA CONSTANTS
LISTINGS_DB = 'listings'
LISTINGS_DB_COLUMNS = ['address', 
              'price', 
              'district', 
              'housing', 
              'beds', 
              'baths', 
              'pets', 
              'in_unit_laundry', 
              'in_building_laundry', 
              'sq_ft', 
              'last_updated', 
              'link']
LISTING_DICT = {
    'address': None, 
    'price': None, 
    'district': None, 
    'housing': None, 
    'beds': None, 
    'baths': None, 
    'pets': None, 
    'in_unit_laundry': None, 
    'in_building_laundry': None, 
    'sq_ft': None, 
    'last_updated': None, 
    'link': None
}

# DB QUERIES
CREATE_TABLES_QUERY = """CREATE TABLE IF NOT EXISTS listings (
    address text PRIMARY KEY, 
    price text, 
    district text, 
    housing text , 
    beds text, 
    baths text, 
    pets text , 
    in_unit_laundry text, 
    in_building_laundry text, 
    sq_ft text, 
    last_updated text, 
    link text
)"""
INSERT_MANY_LISTINGS_QUERY = 'INSERT INTO {} VALUES({}) ON CONFLICT(address) DO UPDATE SET last_updated=excluded.last_updated'.format(
    LISTINGS_DB, ','.join(['?' for i in range(len(LISTINGS_DB_COLUMNS))]))
SELECT_ALL_LISTINGS_QUERY = "SELECT * FROM {}".format(LISTINGS_DB)

# Take a list of listings and return a list of dicts of listings mapping DB columns to values
# TODO: Have listings already as dicts in web?
def map_listings_to_dicts(listings):
    listing_dicts = []
    filters = get_filters()
    for listing in listings:
        listing_dict = LISTING_DICT.copy()
        listing_dict['link'] = listing[0]
        listing_dict['housing'] = listing[1]
        listing_dict['district'] = listing[2]
        listing_dict['address'] = listing[3]
        listing_dict['price'] = listing[4]
        listing_dict['beds'] = listing[5]
        listing_dict['baths'] = listing[6]
        listing_dict['sq_ft'] = listing[7]
        listing_dict['last_updated'] = str(date.today())
        listing_dict['pets'] = 'yes' if is_valid_filter(filters['pets']) else None
        listing_dict['in_unit_laundry'] = 'yes' if is_valid_filter(filters['laundry']['in_unit']) else None
        listing_dict['in_building_laundry'] = 'yes' if is_valid_filter(filters['laundry']['in_building']) else None
        listing_dicts.append(listing_dict)
    return listing_dicts

# Take a list of dicts of listings, return list of tuples of listings that can be directly inserted into DB
def listings_dicts_to_tuples(listings):
    listings_tuples = []
    for listing in listings:
        listings_tuples.append((
           listing['address'],
           listing['price'],
           listing['district'],
           listing['housing'],
           listing['beds'],
           listing['baths'],
           listing['pets'],
           listing['in_unit_laundry'],
           listing['in_building_laundry'],
           listing['sq_ft'],
           listing['last_updated'],
           listing['link']
        ))
    return listings_tuples

