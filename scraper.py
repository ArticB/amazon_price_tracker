import requests
import re
from bs4 import BeautifulSoup


def get_converted_price(price):

    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price)) # Thanks to https://medium.com/@oorjahalt
    return converted_price


def extract_url(url):

    if url.find("www.amazon.in") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url


def get_product_details(url):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}
    _url = extract_url(url)
    if _url is None:
        details = None
    else:
        page = requests.get(_url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url
        else:
            details = None
    return details

# print(get_product_details("https://www.amazon.in/Test-Exclusive-521/dp/B077Q42J32/ref=br_msw_pdt-2?_encoding=UTF8&smid=A14CZOWI0VEHLG&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_s=&pf_rd_r=RSHQJHF4YH8ZQJJRNXH3&pf_rd_t=36701&pf_rd_p=9806b2c4-09c8-4373-b954-bae25b7ea046&pf_rd_i=desktop"))
print(get_product_details("https://www.amazon.in/gp/product/B00IJRV2D0?pf_rd_p=f2b20090-067d-415f-953d-b8dcecc9109f&pf_rd_r=VFJ98F93X80YWYQNR3GN"))
#print(get_product_details("https://www.amazon.com/YI-1080P60-Dashboard-G-Sensor-Recording/dp/B01C89GCHU/ref=br_asw_pdt-3?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=ZRGF7W6FRMPM7YHH4ENK&pf_rd_t=36701&pf_rd_p=143861b7-0857-4329-b93d-3eeedb5f1ea9&pf_rd_i=desktop"))