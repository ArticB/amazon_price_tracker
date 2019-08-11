import db
import scraper
import time

URL = "https://www.amazon.in/dp/B077Q42J32/"

def run():
    details = scraper.get_product_details(URL)
    result = ""
    if details is None:
        result = "not done"
    else:
        inserted = db.add_product_detail(details)
        if inserted:
            result = "done"
        else:
            result = "not done"
    return result

while True:
    print(run())
    time.sleep(60)