import pathlib
import requests
import pandas as pd
from string import Template

DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data")

wearable_sales_query = Template("""
{
    erc1155Purchases(
      first: 1000,
      skip: $skip,
      where: {
       category: 0,
       quantity_gt: 0
      },
      orderBy:timeLastPurchased,
      orderDirection:desc
    ) {
      id
      priceInWei
      erc1155TypeId
      timeLastPurchased
      quantity
      seller
      buyer
      listingID
    }
  }
""")

def run_query(query):
    request = requests.post('https://api.thegraph.com/subgraphs/name/aavegotchi/aavegotchi-core-matic', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def json_to_df(json):
    return pd.json_normalize(json['data']['erc1155Purchases'])



wearable_sales = pd.DataFrame()
for i in range(10):
    skip = i * 1000
    data = json_to_df(run_query(wearable_sales_query.substitute(skip=skip)))
    if len(data) > 0:
        wearable_sales = wearable_sales.append(data)
    else: break


wearable_sales['priceInWei'] = wearable_sales['priceInWei'].astype(float)
wearable_sales['Price (GHST)'] = wearable_sales['priceInWei'] / 1e18
wearable_sales['Date'] = pd.to_datetime(wearable_sales['timePurchased'], unit='s')
wearable_sales = wearable_sales.drop(columns=['priceInWei', 'timePurchased'], axis=1)

wearables_data_url = 'https://raw.githubusercontent.com/programmablewealth/aavegotchi-stats/master/src/data/wearables/wearables.json'
wearables_data = requests.get(wearables_data_url).json()
wearables_name = {i:wearables_data[str(i)]["0"] for i in wearables_data}

#wearable_sales['Body Item'] = wearable_sales['Body'].apply(lambda x: 'NaN' if x == 0 else wearables_data[str(x)]["0"])


wearable_sales.to_csv(DATA_PATH.joinpath('wearable_sales.csv'))