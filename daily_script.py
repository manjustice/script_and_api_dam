from urllib.parse import urljoin

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import schedule
from sqlalchemy import exists
import time

from config import db, app
from models import Date, DAMResult


BASE_URL = "https://www.oree.com.ua/"
CLOSING_TIME = "12:30"


def save_to_db(instance: db.Model) -> db.Model | None:
    with app.app_context():
        db.session.add(instance)
        db.session.commit()

        if instance.__class__ == Date:
            db.session.refresh(instance)
            return instance


def parse_json(soup: BeautifulSoup, date: datetime):
    if soup.find("div", class_="bs-callout-warning") is not None:
        print(f"As of {datetime.now()} calculations have not yet been made")
        time.sleep(60)
        get_json()

    with app.app_context():
        date_exists = (
            db.session.query(
                exists().where(Date.date_value == date.strftime("%Y-%m-%d"))
            ).scalar()
        )

    if date_exists:
        print("This date already exists.")
        return

    date_value = save_to_db(Date(date_value=date))

    for tr in soup.find("tbody").find_all("tr"):
        fields = [
            field.text.strip()
            for field in tr.find_all("td")[1:7]
        ]
        save_to_db(DAMResult(
            hour=int(fields[0]),
            price=float(fields[1]),
            sales_volume=float(fields[2]),
            purchase_volume=float(fields[3]),
            declared_sales_volume=float(fields[4]),
            declared_purchase_volume=float(fields[5]),
            date_id=date_value.id
        ))


def get_json():
    date_tomorrow = (datetime.now() + timedelta(days=1))
    date_to_str = date_tomorrow.strftime("%d.%m.%Y")
    get_hdata_url = f"index.php/PXS/get_pxs_hdata/{date_to_str}/DAM/2"

    response = requests.post(urljoin(BASE_URL, get_hdata_url), verify=False)

    soup = BeautifulSoup(response.json()["html"], "html.parser")

    parse_json(soup, date_tomorrow)


if __name__ == "__main__":
    schedule.every().day.at(CLOSING_TIME).do(get_json)

    while True:
        schedule.run_pending()
        time.sleep(1)
