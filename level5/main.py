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

    daily_price = 0
    for i in range(days):
        if i < 1:
            daily_price += car["price_per_day"]
        elif i < 4:
            # price per day decreases by 10% after 1 day
            daily_price += car["price_per_day"] * 0.9
        elif i < 10:
            # price per day decreases by 30% after 4 days
            daily_price += car["price_per_day"] * 0.7
        else:
            # price per day decreases by 50% after 10 days
            daily_price += car["price_per_day"] * 0.5

    # compute the price of the rental
    price = daily_price + rental["distance"] * car["price_per_km"]

    # compute options
    options = [options["type"] for options in data["options"]
               if options["rental_id"] == rental["id"]]

    owner_additional_money = 0
    if "gps" in options:
        owner_additional_money += 500 * days
    if "baby_seat" in options:
        owner_additional_money += 200 * days

    drivy_additional_money = 0
    if "additional_insurance" in options:
        drivy_additional_money = 1000 * days

    # compute commission
    commission = price * 0.3
    insurance_fee = commission / 2
    assistance_fee = days * 100
    drivy_fee = insurance_fee - assistance_fee

    rentals["rentals"].append({
        "id": rental["id"],
        "options": options,
        "actions": [
            {
                "who": "driver",
                "type": "debit",
                "amount": price + owner_additional_money + drivy_additional_money
            },
            {
                "who": "owner",
                "type": "credit",
                "amount": price - commission +
                              owner_additional_money
            },
            {
                "who": "insurance",
                "type": "credit",
                "amount": insurance_fee
            },
            {
                "who": "assistance",
                "type": "credit",
                "amount": assistance_fee
            },
            {
                "who": "drivy",
                "type": "credit",
                "amount": drivy_fee + drivy_additional_money
            }
        ]
    })

# Check

assert rentals == expected_output
