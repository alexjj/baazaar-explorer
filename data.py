# One day replace with database / caching API calls etc.
# Maybe this https://realpython.com/lru-cache-python/

import pathlib
import pandas as pd

DATA_PATH = pathlib.Path(__file__).parent.joinpath("data")

gotchi_sales = pd.read_csv(DATA_PATH.joinpath("gotchi_sales.csv"))
ticket_sales = pd.read_csv(DATA_PATH.joinpath("ticket_sales.csv"))
wearable_sales = pd.read_csv(DATA_PATH.joinpath("wearable_sales.csv"))
# Can also add functions and hard coded lists etc. here