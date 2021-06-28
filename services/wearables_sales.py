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
for i in range(5):
    skip = i * 1000
    data = json_to_df(run_query(wearable_sales_query.substitute(skip=skip)))
    if len(data) > 0:
        wearable_sales = wearable_sales.append(data)
    else: break


wearable_sales['priceInWei'] = wearable_sales['priceInWei'].astype(float)
wearable_sales['Price (GHST)'] = wearable_sales['priceInWei'] / 1e18
wearable_sales['Date'] = pd.to_datetime(wearable_sales['timeLastPurchased'], unit='s')
wearable_sales = wearable_sales.drop(columns=['priceInWei', 'timeLastPurchased'], axis=1)

wearables_data_url = 'https://raw.githubusercontent.com/programmablewealth/aavegotchi-stats/master/src/data/wearables/wearables.json'
wearables_data = requests.get(wearables_data_url).json()
wearables_name = {i:wearables_data[str(i)]["0"] for i in wearables_data}
wearable_sales['Name'] = wearable_sales['erc1155TypeId'].apply(lambda x: '' if x == 0 else wearables_data[str(x)]["0"])
wearable_sales['Max Quantity'] = wearable_sales['erc1155TypeId'].apply(lambda x: '' if x == 0 else wearables_data[str(x)]["9"])
wearable_sales['Original Price (GHST)'] = wearable_sales['erc1155TypeId'].apply(lambda x: '' if x == 0 else wearables_data[str(x)]["7"])
wearable_sales['Original Price (GHST)'] = wearable_sales['Original Price (GHST)'].astype(float) / 1e18
wearable_sales['Slot List'] = wearable_sales['erc1155TypeId'].apply(lambda x: '' if x == 0 else wearables_data[str(x)]["4"])

def wearable_rarity(maxquantity):
    if maxquantity >= 1000:
        return "Common"
    elif maxquantity >= 500:
        return "Uncommon"
    elif maxquantity >= 250:
        return "Rare"
    elif maxquantity >= 100:
        return "Legendary"
    elif maxquantity >= 10:
        return "Mythical"
    elif maxquantity >= 1:
        return "Godlike"

wearable_sales = wearable_sales.rename(columns={"listingID": "Listing", "buyer": "Buyer", "seller": "Seller",
"quantity": "Quantity", })
wearable_sales['Quantity'] = wearable_sales['Quantity'].apply(pd.to_numeric, errors='coerce')
wearable_sales['Rarity'] = wearable_sales['Max Quantity'].astype(float).apply(lambda x: wearable_rarity(x))
wearable_sales['Total Purchase (GHST)'] = wearable_sales['Price (GHST)'] * wearable_sales['Quantity']

def which_slot(slot_list):
    if slot_list[0]: return "Body"
    elif slot_list[1]: return "Face"
    elif slot_list[2]: return "Eyes"
    elif slot_list[3]: return "Head"
    elif slot_list[4]: return "Hand"
    elif slot_list[5]: return "Hand"
    elif slot_list[6]: return "Pet"
    elif slot_list[7]: return "Background"
    else:
        return "Unknown"

wearable_sales['Slot'] = wearable_sales['Slot List'].apply(lambda x: which_slot(x))

wearable_sales = wearable_sales.drop(columns=['Slot List', 'Max Quantity', 'id', 'erc1155TypeId'], axis=1)

wearable_sales.to_csv(DATA_PATH.joinpath('wearable_sales.csv'))