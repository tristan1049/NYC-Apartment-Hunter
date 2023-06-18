from web import get_listings

if __name__ == '__main__':
    for listings in get_listings():
        for listing in listings:
            print(listing)