import os
import functions_framework
from http.client import METHOD_NOT_ALLOWED
from dataclasses import dataclass
from urllib.request import urlopen
from os import getenv
from pypdf import PdfReader
from ast import literal_eval
from io import BytesIO
import json

prod = literal_eval(os.environ["PROD"])


@dataclass
class Product:
    _id: str = ""
    _name: str = ""
    _price: str = ""
    _category: str = ""
    _gst: str = ""

    @property
    def id(self):
        return int(literal_eval(self._id.replace("+", "")))

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        if self._price.lower() != "ask":
            return int(self._price)
        return self._price.upper()

    @property
    def category(self):
        return self._category

    @property
    def gst(self):
        return int(self._gst)

    @property
    def is_complete(self):
        return self._id and self._name and self._price

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            category=self.category,
            gst=self.gst,
        )

    def __str__(self) -> str:
        return "\t".join(
            [str(self.id), self.name, str(self.price), self.category, str(self.gst)]
        )


COL_DIST = 185.27999499999999
FIRST_COL = 49.119999


def gen_range(n: int, a=-4, b=10):
    col = COL_DIST * n + FIRST_COL
    return range(int(col + a), int(col + b))


def gen_range_list(a, b):
    return tuple(gen_range(x, a, b) for x in range(4))


FOUR_COL_TEXT_RANGE = gen_range_list(-4, 10)
FOUR_COL_ID_RANGE = gen_range_list(-40, -10)
FOUR_COL_PRICE_RANGE = gen_range_list(110.881, 150.881)


def compare_true(x: int, range_var: tuple[range, range, range, range]):
    return any([x in r for r in range_var])


parts = [Product()]
category = ""
gst_bracket = ""


def visitor_body(text: str, cm, tm, fontDict, fontSize):
    text = text.strip()

    global category
    global gst_bracket
    if "%" in text:
        category = text[:-3].strip()
        gst_bracket = text[-1 - 2 : -1]

    x = tm[4]
    y = tm[5]
    if not text or "\n" in text or "%" in text or y < 200:
        return
    x = int(x)

    item = parts[-1]

    # text
    if compare_true(x, FOUR_COL_TEXT_RANGE):
        if item.is_complete:
            parts.append(Product())
            item = parts[-1]
        item._name += text

    if (
        text.lower().isdigit()
        or "ask" in text.lower()
        or "E+03" in text
        or text.endswith("..")
        or text.endswith("…")
    ):
        # number
        if compare_true(x, FOUR_COL_ID_RANGE):
            item._id = text
            item._category = category
            item._gst = gst_bracket

        # price
        if compare_true(x, FOUR_COL_PRICE_RANGE) or "ask" in text.lower():
            item._price = text.replace("..", "").replace("…", "")


# Register an HTTP function with the Functions Framework
def get_pricelist_json():
    if prod:
        with urlopen("http://www.costtocost.in/list/pricelist.pdf") as u:
            data = u.read()
            reader = PdfReader(BytesIO(data))
    else:
        reader = PdfReader("../try_rust/data/pricelist.pdf")
    for page in reader.pages:
        page.extract_text(visitor_text=visitor_body)
    return_json = json.dumps(list(map(lambda x: x.serialize(), parts)))
    parts.clear()
    headers = {"Access-Control-Allow-Origin": "*", "Content-type": "application/json"}
    return (return_json, 200, headers)


@functions_framework.http
def get_pricelist_json_gcloud(request):
    if request.method != "GET":
        return ("Only Get Method Allowed", METHOD_NOT_ALLOWED, {})
    return get_pricelist_json()


if __name__ == "__main__":
    if not prod:
        print(get_pricelist_json())
