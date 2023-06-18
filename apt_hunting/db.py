import sqlite3

from utils.db_utils import map_listings_to_dicts
from utils.db_utils import listings_dicts_to_tuples
from utils.db_utils import CREATE_TABLES_QUERY
from utils.db_utils import INSERT_MANY_LISTINGS_QUERY
from utils.db_utils import SELECT_ALL_LISTINGS_QUERY

def get_conn():
    return sqlite3.connect('listings.db')

def close_conn(conn):
    conn.close()

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLES_QUERY)

def insert_many_listings(conn, data):
    cursor = conn.cursor()
    cursor.executemany(INSERT_MANY_LISTINGS_QUERY, data)
    conn.commit()
    return cursor.rowcount

def select_all_listings(conn):
    cursor = conn.cursor()
    result = cursor.execute(SELECT_ALL_LISTINGS_QUERY)
    return result.fetchall()

def insert_listings_to_db(conn, listings):
    create_tables(conn)
    listings_dicts = map_listings_to_dicts(listings)
    listings_tuples = listings_dicts_to_tuples(listings_dicts)
    insert_many_listings(conn, listings_tuples)
    return listings_tuples

if __name__ == '__main__':
    get_conn()