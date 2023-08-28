import requests
import re
import pandas as pd

# Shopee API
SHOPEE_API_URL = '''https://shopee.com.my/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit=20&offset={offset}&shopid={shop_id}&type=0'''
shop_id = ""
item_id = ""
item = {}
LIMIT = 500

def get_product_details():
    return item

def get_product_id(URL):
    # Get shop id and item id from input URL
    r = re.search(r"i\.(\d+)\.(\d+)", URL)
    shop_id, item_id = r[1], r[2]
    return shop_id, item_id

def scrape(URL):
    try:
        shop_id, item_id = get_product_id(URL)
    except:
        return None

    offset = 0
    review = {"rating": [], "comment": []}
    while True:
        # Get JSON data using shop_id and item_id from input URL
        data = requests.get(
            SHOPEE_API_URL.format(shop_id=shop_id, item_id=item_id, offset=offset)
        ).json()
        
        i = 1
        ratings = data["data"]["ratings"]
        for i, scraped in enumerate(ratings, 1):
            review["rating"].append(scraped["rating_star"])
            review["comment"].append(scraped["comment"])

        if i % 20:
            break

        offset += 20
        if(offset >= LIMIT):
            break

    df = pd.DataFrame(review)
    
    return df

def get_overall_rating(df):
    # round rating to 2 decimal points
    total = df["rating"].count()
    rating = df["rating"].mean().__round__(2)
    return rating, total