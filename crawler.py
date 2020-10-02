from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.request import Request
from urllib import error
import pandas as pd


def get_items_data():
    page_url = "https://oilsisrael.com/product-category/essential-oil/page/1"
    item_list = []

    try:
        while 1:
            req = Request(
                page_url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
                }
            )

            uClient = uReq(req)
            page_soup = soup(uClient.read(), "html.parser")
            uClient.close()

            # get each product
            containers = page_soup.findAll("div", {"class": "product-small box"})

            for container in containers:
                # get item name
                item_name = container.findAll("div", {"class": "title-wrapper"})[0].a.text
                # get lowest price of product
                item_min_price = container.findAll("span",{"class":"woocommerce-Price-amount amount"})[0].bdi.text
                item_min_price = item_min_price[:-2]
                item_list.append([item_name, float(item_min_price)])

            page_url = page_soup.findAll("a", {"class": "next"})[0].attrs['href']

    except error.HTTPError as e:
        print("No next page - Finished collecting items")
    except IndexError as e:
        print("No next page - Finished collecting items")
    finally:
        df = pd.DataFrame(item_list, columns=['Item_Name', 'Item_Price'])
        df = df.sort_values(by="Item_Price")
        df.to_csv(r'/Users/shai/Documents/python_projects/Essential-essential-oils/essential_oils.csv', index=False)


if __name__ == "__main__":
    get_items_data()

