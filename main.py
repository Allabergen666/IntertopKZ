# Created modules
import json
from os import getenv, system

# Downloaded libraries
import requests
from bs4 import BeautifulSoup

# Created modyle
from core.config import URL, DOMAIN, HEADERS


def get_html(url, headers):
    responce = requests.get(url, headers=headers)
    if responce.status_code == 200:
        return responce.text
    else:
        return f"error: {responce.status_code}"
    

def processing_response(response):
    soup = BeautifulSoup(response, "lxml").find(
        "div", {"class": "items load-more-elements-wrapper"}).find_all("a")
    
    data = []
    
    for item in soup:
        product_name = item.get("data-name")
        product_url = DOMAIN + item.get("href")
        product_category = item.find("div", {"class": "new-product__category"}).find_next_sibling(
        "div", {"class": "new-product__category"}).text
        new_price = str(item.find("div", {"class": "new-product__footer"}).find(
        "span", {"class": "new-product__new-price"}).text).replace("\n", "").strip().replace("\xa0", "")
        try:
            old_price = str(item.find("div", {"class": "old-product__footer"}).find(
            "span", {"class": "new-product__new-price"}).text).replace("\n", "").strip().replace("\xa0", "")
        except:
            old_price  = None

        data.append({
            "name": product_name, 
            "category": product_category, 
            "price": new_price, 
            "old price": old_price, 
            "url": product_url
        })
    return (data)


def runner_parser():
    response = get_html(URL, headers=HEADERS)
    source = processing_response(response)

    with open("core/product.json", "w") as JF:
        json.dump(source, JF, indent=4, ensure_ascii=False)

    # print(source)
runner_parser()