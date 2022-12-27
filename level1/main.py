"""
Level 1
"""

from pathlib import Path
import json
from datetime import date

data_folder = Path(__file__).parent / "data"

# read the data from the file "data/input.json"
with open(data_folder / "input.json",  encoding="UTF-8") as f:
    data = json.load(f)

with open(data_folder / "expected_output.json", encoding="UTF-8") as f:
    expected_output = json.load(f)

# Helpers

def to_date(date_str):
    """ Convert a string (YYYY-MM-DD) to a date """
    return date(*map(int, date_str.split("-")))

# Code

rentals = {"rentals": []}

for rental in data["rentals"]:
    # get the car corresponding to the rental
    car = next(car for car in data["cars"] if car["id"] == rental["car_id"])

    # get the number of days of the rental
    days = (to_date(rental["end_date"]) -
            to_date(rental["start_date"])).days + 1

    # compute the price of the rental
    rentals["rentals"].append({
        "id": rental["id"],
        "price": days * car["price_per_day"] + rental["distance"] * car["price_per_km"]
    })

# Check

assert rentals == expected_output
