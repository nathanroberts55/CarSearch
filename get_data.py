import pandas as pd
import numpy as np
from dataclasses import dataclass
import requests
from datetime import datetime
from logger import logger


@dataclass
class UsedCar:
    make: str
    model: str
    year: str
    price: str
    dealership: str
    dealer_address: str
    dealer_city: str
    dealer_state: str
    dealer_zip: str
    distance: float
    url: str
    mileage: str = 0


def get_vehicle_data(make, zip, radius, priceMax, yearMin):
    try:
        logger.info(
            f"Making Request to Carfax API for - Make: {make}, Zip: {zip}, Radius: {radius}, Max Price: {priceMax}, Min Year: {yearMin},"
        )
        url = f"https://helix.carfax.com/search/v2/vehicles?zip={zip}&radius={radius}&sort=BEST&make={make}&certified=false&vehicleCondition=USED&bodyType=SUV&mileageMax=100000&priceMax={priceMax}&yearMin={yearMin}&dynamicRadius=false&tpQualityThreshold=150&tpPositions=1%2C2%2C3&tpValueBadges=GOOD%2CGREAT&urlInfo=Used-Honda-SUVs_m11_bt8&bodytypes=SUV"
        response = requests.get(url)
    except Exception as e:
        logger.exception(
            f"Unable to make get request to the Carfax Server, Exception: {e}"
        )
    return response.json()


def get_car_df(
    makes: list = ["Honda", "Toyota", "Subaru", "Lexus", "Acura"],
    zip: str = "22030",
    radius: int = 50,
    priceMax=17000,
    yearMin=2009,
):
    all_listings = []
    cars = []

    for make in makes:
        data = get_vehicle_data(
            make=make, zip=zip, radius=radius, priceMax=priceMax, yearMin=yearMin
        )
        all_listings.extend(data["listings"])

    logger.info("Converting Cars to Dataclass Objects")

    for listing in all_listings:
        uc = UsedCar(
            make=listing.get("make", None),
            model=listing.get("model", None),
            year=listing.get("year", None),
            price=listing.get("currentPrice", None),
            mileage=listing.get("mileage", None),
            dealership=listing["dealer"].get("name", None),
            dealer_address=listing["dealer"].get("address", None),
            dealer_city=listing["dealer"].get("city", None),
            dealer_state=listing["dealer"].get("state", None),
            dealer_zip=listing["dealer"].get("zip", None),
            distance=listing.get("distanceToDealer", None),
            url=listing.get("vdpUrl", None),
        )

        cars.append(uc)

    try:
        logger.info("Converting List of Cars to Dataframe")
        cars_df = pd.DataFrame(cars)
    except Exception as e:
        logger.exception(f"Unable to Convert List to Dataframe, Exception: {e}")

    return cars, cars_df


def convert_to_excel(df: pd.DataFrame):
    logger.info("Converting DataFrame to Excel")
    # Get the current date
    current_date = datetime.now()

    # Format the date
    formatted_date = current_date.strftime("%m-%d-%y")
    try:
        logger.info(
            f"Saving Dataframe as Excel at location - data/cars-{formatted_date}.xlsx"
        )
        df.to_excel(f"data/cars-{formatted_date}.xlsx", index=False)
    except Exception as e:
        logger.exception(f"Unable to Saving Dataframe as Excel, Exception: {e}")
