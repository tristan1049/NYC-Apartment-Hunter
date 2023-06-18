import requests
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime

from utils.filters_utils import get_commute_limit
from utils.web_utils import get_streeteasy_url_with_filters
from utils.web_utils import get_commute_time_url
from utils.web_utils import HEADERS
from utils.web_utils import LISTING_CLASS
from utils.web_utils import BUILDING_CLASS
from utils.web_utils import PRICE_CLASS
from utils.web_utils import BEDS_CLASS
from utils.web_utils import BATHS_CLASS
from utils.web_utils import SQ_FT_CLASS

def get_commute_time(address):
    url = get_commute_time_url(address)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    if response.json()['rows'][0]['elements'][0]['status'] == 'NOT_FOUND':
        return None
    return response.json()['rows'][0]['elements'][0]['duration']['text']

def get_listings_one_page(page_num=1):
    rv = []
    response = requests.get(get_streeteasy_url_with_filters(page_num), headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    listings = soup.find_all(class_=LISTING_CLASS) 
    for listing in listings:
        href = listing.a.get('href')
        # Need to use find all as sometimes there are multiple lines, but only the last one has the building information
        building_type = listing.find_all('p', class_=BUILDING_CLASS)[-1]
        housing, district = building_type.string.strip().split(' in ')
        address = listing.find('address').a.string.strip()
        commute = get_commute_time(address)
        price = listing.find('span', class_=PRICE_CLASS).string.strip()
        beds = listing.find('span', class_=BEDS_CLASS).next_sibling.next_sibling.string.strip()
        baths = listing.find('span', class_=BATHS_CLASS).next_sibling.next_sibling.string.strip()
        sq_ft = listing.find('span', class_=SQ_FT_CLASS)
        if (sq_ft):
            sq_ft = sq_ft.next_sibling.next_sibling.contents[0].strip()

        if commute:
            if int(commute.split(' mins')[0]) < get_commute_limit():
                rv.append([href, housing, district, address, commute, price, beds, baths, sq_ft])
        else:
            rv.append([href, housing, district, address, commute, price, beds, baths, sq_ft])

    return rv

# Generator that gets newest listings data for n=pages pages. If None, gets data from all pages
def get_listings(pages=None):
    # Get max number of pages
    first_page = requests.get(get_streeteasy_url_with_filters(1), headers=HEADERS) 
    soup = BeautifulSoup(first_page.text, 'html.parser')
    max_pages = int(soup.find_all('li', class_='page')[-1].a.string.strip())
    time.sleep(2)

    if pages:
        if pages <= 0:
            return
        elif pages > max_pages:
            pages = max_pages
    elif pages == None:
        pages = max_pages

    for page in range(1, pages+1):
        yield get_listings_one_page(page)
        # Sleep for 8-10 seconds to not send too many requests at once
        time.sleep(round(random.uniform(8, 10), 3))
