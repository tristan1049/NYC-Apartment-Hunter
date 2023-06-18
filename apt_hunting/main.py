from db import get_conn
from db import close_conn
from db import insert_listings_to_db
from db import select_all_listings
from web import get_listings

def main():
    # Get DB connection
    conn = get_conn()

    # Receive each set of listings from generator as they come
    for listings in get_listings():
        # Insert the listings into the db
        insert_listings_to_db(conn, listings)
        print(len(select_all_listings(conn)))

    # Once finished, close the connection
    conn.close()

if __name__ == '__main__':
    main()