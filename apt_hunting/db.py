import sqlite3

from utils.db_utils import CREATE_LISTINGS_TABLE_QUERY
from utils.db_utils import CREATE_COMMUTES_TABLE_QUERY
from utils.db_utils import get_listings_with_address_query
from utils.db_utils import get_all_listings_with_filters_query
from utils.db_utils import insert_one_commute_query
from utils.db_utils import insert_one_listing_query
from utils.db_utils import get_commute_with_origin_query
from utils.db_utils import create_listings_tuple
from utils.db_utils import create_commutes_tuple

def get_conn():
    return sqlite3.connect('listings.db')

def close_conn(conn):
    conn.close()

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(CREATE_LISTINGS_TABLE_QUERY)
    cursor.execute(CREATE_COMMUTES_TABLE_QUERY)

def select_all_listings_with_filters(conn):
    cursor = conn.cursor()
    result = cursor.execute(get_all_listings_with_filters_query())
    return result.fetchall()

def insert_one_listing(conn, listing):
    cursor = conn.cursor()
    cursor.execute(insert_one_listing_query(), listing)
    conn.commit()
    return cursor.rowcount 

def insert_one_commute(conn, commute_info):
    cursor = conn.cursor()
    cursor.execute(insert_one_commute_query(), commute_info)
    conn.commit()
    return cursor.rowcount

def select_listings_with_address(conn, address):
    cursor = conn.cursor()
    result = cursor.execute(get_listings_with_address_query(address))
    listing = result.fetchone()
    if listing:
        return listing[0]
    
def select_commute_with_origin(conn, origin):
    cursor = conn.cursor()
    result = cursor.execute(get_commute_with_origin_query(origin))
    commute = result.fetchone()
    if commute:
        return commute[0]

def insert_many_listings(conn, listings):
    inserted = 0
    for listing in listings:
        result = select_listings_with_address(conn, listing['address'])
        # If address not in db, insert listing into db
        if not result:
            inserted += insert_one_listing(conn, create_listings_tuple(listing))
    return inserted

def insert_many_commutes(conn, listings):
    inserted = 0
    for listing in listings:
        result = select_commute_with_origin(conn, listing['address'])
        # If commute not in db, insert commute into db
        if not result:
            inserted += insert_one_commute(conn, create_commutes_tuple(listing))
    return inserted 

def insert_listings_to_db(conn, listings):
    listings_inserted = insert_many_listings(conn, listings)
    commutes_inserted = insert_many_commutes(conn, listings)
    return listings_inserted

if __name__ == '__main__':
    get_conn()