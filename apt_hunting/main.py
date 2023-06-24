from db import get_conn
from db import close_conn
from db import create_tables
from db import insert_listings_to_db
from db import select_all_listings
from web import get_listings
from sheets import create_token
from sheets import build_sheet
from sheets import build_sheet_url
from sheets import insert_sheet
from sheets import get_sheet_id

def main():
    # Get DB connection and create tables
    conn = get_conn()
    create_tables(conn)

    # Get the sheet_id, or create the spreadsheet if not exists
    creds = create_token() 
    sheet_id = get_sheet_id(creds)
    sheet_url = build_sheet_url(sheet_id)
    print("NYC Apartment Findings Spreadsheet: \n{}".format(sheet_url))

    # Receive each set of listings from generator as they come
    for listings in get_listings():
        # Insert the listings into the db
        rows_inserted = insert_listings_to_db(conn, listings)
        all_listings = select_all_listings(conn)
        print("Inserted {} listings".format(rows_inserted))

        # Insert the unique listings into a spreadsheet
        insert_sheet(creds, sheet_id, all_listings)

    # Once finished, close the connection
    close_conn(conn)

if __name__ == '__main__':
    main()