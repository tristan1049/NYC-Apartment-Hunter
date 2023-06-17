import requests
from bs4 import BeautifulSoup

from utils.web import HEADERS
from utils.web import STREETEASY_URL
from utils.web import LISTING_CLASS
from utils.web import BUILDING_CLASS
from utils.web import PRICE_CLASS
from utils.web import BEDS_CLASS
from utils.web import BATHS_CLASS
from utils.web import SQ_FT_CLASS

def get_listings():
    rv = []
    response = requests.get(STREETEASY_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = soup.find_all(class_=LISTING_CLASS) 
    for listing in listings:
        href = listing.a.get('href')
        # Need to use find all as sometimes there are multiple lines, but only the last one has the building information
        building_type = listing.find_all('p', class_=BUILDING_CLASS)[-1]
        housing, district = building_type.string.strip().split(' in ')
        address = listing.find('address').a.string.strip()
        price = listing.find('span', class_=PRICE_CLASS).string.strip()
        beds = listing.find('span', class_=BEDS_CLASS).next_sibling.next_sibling.string.strip()
        baths = listing.find('span', class_=BATHS_CLASS).next_sibling.next_sibling.string.strip()
        sq_ft = listing.find('span', class_=SQ_FT_CLASS)
        if (sq_ft):
            sq_ft = sq_ft.next_sibling.next_sibling.contents[0].strip()

        rv.append([href, housing, district, address, price, beds, baths, sq_ft])

    return rv

if __name__ == '__main__':
    listings_info = get_listings()
    for listing in listings_info:
        print(listing)