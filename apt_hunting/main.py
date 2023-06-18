from db import get_conn
from db import close_conn
from db import insert_listings_to_db
from web import get_listings
from sheets import create_token
from sheets import build_sheet
from sheets import build_sheet_url
from sheets import append_sheet

def main():
    # Get DB connection
    conn = get_conn()

    # Create the spreadsheet
    creds = create_token() 
    sheet_id = build_sheet(creds, "NYC Apartments")
    sheet_url = build_sheet_url(sheet_id)
    print("NYC Apartment Findings Spreadsheet: \n{}".format(sheet_url))

    # Receive each set of listings from generator as they come
    for listings in get_listings():
        # Insert the listings into the db
        rows_inserted = insert_listings_to_db(conn, listings)
        append_sheet(creds, sheet_id, rows_inserted)
        # print(len(select_all_listings(conn)))

    # Once finished, close the connection
    close_conn(conn)

if __name__ == '__main__':
    main()