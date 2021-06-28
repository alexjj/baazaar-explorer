import pathlib
import requests
import pandas as pd
from string import Template

DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data")

# 5000 is max skip

ticket_sales_query = Template("""
{
    erc1155Purchases(
      first: 1000,
      skip: $skip,
      where: {
       category: 3,
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


ticket_sales = pd.DataFrame()
for i in range(5):
    skip = i * 1000
    data = json_to_df(run_query(ticket_sales_query.substitute(skip=skip)))
    if len(data) > 0:
        ticket_sales = ticket_sales.append(data)
    else: break

ticket_sales['priceInWei'] = ticket_sales['priceInWei'].astype(float)
ticket_sales['Price per Ticket (GHST)'] = ticket_sales['priceInWei'] / 1e18
ticket_sales['Date'] = pd.to_datetime(ticket_sales['timePurchased'], unit='s')
ticket_sales = ticket_sales.drop(columns=['priceInWei', 'timePurchased'], axis=1)

replace_values = {
    '0': 'Common',
    '1': 'Uncommon',
    '2': 'Rare',
    '3': 'Legendary',
    '4': 'Mythical',
    '5': 'Godlike',
}

ticket_sales['erc1155TypeId'] = ticket_sales['erc1155TypeId'].replace(replace_values, regex=True)

ticket_sales = ticket_sales.rename(columns={"listingID": "Listing", "buyer": "Buyer", "seller": "Seller",
"quantity": "Quantity", "erc1155TypeId": "Type", })

ticket_sales['Total Purchase (GHST)'] = ticket_sales['Price per Ticket (GHST)'] * ticket_sales['Quantity']

ticket_sales.to_csv(DATA_PATH.joinpath('ticket_sales.csv'))