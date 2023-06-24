from datetime import date

from utils.filters_utils import get_filters
from utils.filters_utils import is_valid_filter

# DB METADATA CONSTANTS
LISTINGS_DB = 'listings'
COMMUTES_DB = 'commutes'
LISTINGS_DB_COLUMNS = [
    'address',       
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
    'link'
]
COMMUTES_DB_COLUMNS = [
    'origin',
    'destination',
    'mode',
    'commute'
]
LISTINGS_COMMUTES_JOIN_COLUMNS = [
    'listings.address',
    'commutes.destination',
    'commutes.commute',
    'commutes.mode',
    'listings.price',
    'listings.district',
    'listings.housing',
    'listings.beds',
    'listings.baths',
    'listings.pets',
    'listings.in_unit_laundry',
    'listings.in_building_laundry',
    'listings.sq_ft',
    'listings.last_updated',
    'listings.link',
]

# DB QUERIES
CREATE_LISTINGS_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS {} (
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
)""".format(LISTINGS_DB)
CREATE_COMMUTES_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS {} (
    origin text,
    destination text,
    mode text,
    commute text
)""".format(COMMUTES_DB)

def get_listings_with_address_query(address):
    return "SELECT address FROM {} WHERE address = '{}'".format(LISTINGS_DB, address)

def get_commute_with_origin_query(origin):
    filters = get_filters()
    dest = filters['commute']['address']
    mode = filters['commute']['mode_transportation']
    return "SELECT commute FROM {} WHERE origin = '{}' and destination = '{}' and mode = '{}'".format(
        COMMUTES_DB, origin, dest, mode
    )

def get_all_listings_with_filters_query():
    filters = get_filters()
    return "SELECT {} FROM {} INNER JOIN {} ON {}.address = {}.origin \
            WHERE {}.destination = '{}' AND {}.mode = '{}'".format(
        ",".join(LISTINGS_COMMUTES_JOIN_COLUMNS),
        LISTINGS_DB,
        COMMUTES_DB,
        LISTINGS_DB,
        COMMUTES_DB,
        COMMUTES_DB,
        filters['commute']['address'],
        COMMUTES_DB,
        filters['commute']['mode_transportation']
    )

def insert_one_listing_query():
    return "INSERT INTO {} VALUES({})".format(
        LISTINGS_DB,
        ",".join(["?" for i in range(len(LISTINGS_DB_COLUMNS))]))

def insert_one_commute_query():
    return "INSERT INTO {} VALUES ({})".format(
        COMMUTES_DB,
        ",".join(["?" for i in range(len(COMMUTES_DB_COLUMNS))]))

def create_listings_tuple(listing):
    filters = get_filters()
    return (
        listing['address'],
        listing['price'],
        listing['district'],
        listing['housing'],
        listing['beds'],
        listing['baths'],
        'yes' if is_valid_filter(filters['pets']) else None,
        'yes' if is_valid_filter(filters['laundry']['in_unit']) else None,
        'yes' if is_valid_filter(filters['laundry']['in_building']) else None,
        listing['sq_ft'],
        str(date.today()),
        listing['link']
    )

def create_commutes_tuple(listing):
    filters = get_filters()
    return (
        listing['address'],
        filters['commute']['address'],
        filters['commute']['mode_transportation'],
        listing['commute']
    )
