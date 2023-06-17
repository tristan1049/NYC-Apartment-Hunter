# NYC-Apartment-Hunter
This project was made to help simplify the apartment hunting process in NYC. Listings come from StreetEasy. Work in Progress.

## Advantages
Advantages of using this tool to find apartment listings:
- Automatically sends large amounts of unique listings matching filters to a Google Sheet for easy data filtering and visualization in one spreadsheet. (Not available yet)
- Integrated with the Google Maps API to also allow filtering by commute time from address to your workplace. (Not available yet)
- Run in the background of your system to catch any new listings at any time (Not available yet)

## Setup
First, source into the provided environment or any environment of your choosing:
```
$ source env/bin/activate
```

Then, run the `requirements.txt` file to gather necessary imports:
```
$ pip install -r requirements.txt
```

Now you should be good to go! To get data for one page of listings, run this command (More features in the future):
```
$ python3 apt_hunting/main.py
```