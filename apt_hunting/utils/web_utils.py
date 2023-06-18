# REQUESTS CONSTANTS
STREETEASY_URL = "https://streeteasy.com/for-rent/nyc?sort_by=listed_desc"
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

def get_streeteasy_url(page_num=1):
    return STREETEASY_URL + '&page={}'.format(str(page_num))