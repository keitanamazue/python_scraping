
from fastapi import FastAPI
import urllib.parse
import re
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from mangum import Mangum


app = FastAPI()

@app.get("/")
async def root():
    yodobashi_url = "https://www.yodobashi.com"

    url_params = {"word": "PS4コントローラーレッド"}
    req_url = yodobashi_url + "/?" + urllib.parse.urlencode(url_params)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        "referer":yodobashi_url,
        'Accept-Language': 'ja,en-us;q=0.7,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }


    try:
        res = requests.get(req_url, headers=headers)
        res.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to http request:", e)
    else:
        product_datas = []

        soup = BeautifulSoup(res.text, "html.parser")
        for item in soup.find_all("div", class_="productListTile"):
            a = item.find(href=re.compile("/product/"))
            product_url = yodobashi_url + a.attrs['href']
            product_name = a.find("img").attrs['alt']
            product_price = item.find("ul", class_="js_addLatestSalesOrder").find(string=re.compile("￥"))
            product_datas.append({
                "name": product_name,
                "price": product_price,
                "url": product_url,
            })
            
    return product_datas

handler = Mangum(app)