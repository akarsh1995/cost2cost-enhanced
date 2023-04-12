import os
from typing import List, Optional
import functions_framework
from http.client import METHOD_NOT_ALLOWED
from dataclasses import dataclass, field, asdict
from urllib.request import urlopen
from pypdf import PdfReader
from ast import literal_eval
from io import BytesIO
import json
from upload import upload_blob_from_memory
import gzip

prod = literal_eval(os.environ["PROD"])


def clean_id(id: str):
    return int(literal_eval(id.replace("+", "")))


def clean_price(price: str):
    price = price.replace("..", "").replace("…", "")
    if price.lower() != "ask":
        return int(price)
    return 0


def clean_gst(gst_rate: str):
    return int(gst_rate)


@dataclass
class Product:
    id: int = 0
    name: str = ""
    price: Optional[int] = None

    @property
    def is_complete(self):
        return self.id and self.name

    def __str__(self) -> str:
        return "\t".join([str(self.id), str(self.name), str(self.price)])


@dataclass
class Category:
    category: str = ""
    gst: int = 0
    products: List[Product] = field(default_factory=list)

    def add_product(self, pro: Product):
        self.products.append(pro)


@dataclass
class CategorisedProducts:
    data: List[Category] = field(default_factory=list)


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


categorised_products = CategorisedProducts()
current_product = Product()
category = Category()


def visitor_body(text: str, cm, tm, fontDict, fontSize):
    text = text.strip()

    global current_product
    global category
    global gst_bracket
    if "%" in text:
        if current_product.is_complete:
            category.add_product(current_product)
        categorised_products.data.append(
            Category(
                category=text[:-3].strip(),
                gst=int(text[-1 - 2 : -1]),
            )
        )
        current_product = Product()
        category = categorised_products.data[-1]

    x = tm[4]
    y = tm[5]
    if not text or "\n" in text or "%" in text or y < 200:
        return
    x = int(x)

    # text
    if compare_true(x, FOUR_COL_TEXT_RANGE):
        if current_product.is_complete:
            category.add_product(current_product)
            current_product = Product()
        current_product.name += text

    if (
        text.lower().isdigit()
        or "ask" in text.lower()
        or "E+03" in text
        or text.endswith("..")
        or text.endswith("…")
    ):
        # number
        if compare_true(x, FOUR_COL_ID_RANGE):
            current_product.id = clean_id(text)

        # price
        if compare_true(x, FOUR_COL_PRICE_RANGE) or "ask" in text.lower():
            current_product.price = clean_price(text)


def get_pricelist():
    global categorised_products
    global current_product
    global category
    categorised_products = CategorisedProducts()
    current_product = Product()
    category = Category()

    if prod:
        with urlopen("http://www.costtocost.in/list/pricelist.pdf") as u:
            data = u.read()
            reader = PdfReader(BytesIO(data))
    else:
        reader = PdfReader("../../try_rust/data/pricelist.pdf")
    for page in reader.pages:
        page.extract_text(visitor_text=visitor_body)
    categorised_products.data[-1].add_product(current_product)
    return asdict(categorised_products)


# Register an HTTP function with the Functions Framework
def get_pricelist_json_out():
    return_json = json.dumps(get_pricelist())
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
        "Content-Encoding": "gzip",
    }
    return (gzip.compress(return_json.encode()), 200, headers)


@functions_framework.http
def get_pricelist_json(request):
    if request.method != "GET":
        return ("Only Get Method Allowed", METHOD_NOT_ALLOWED, {})
    r = get_pricelist_json_out()
    upload_blob_from_memory(
        os.environ["BUCKET_ID"],
        r[0],
        "price.json",
        {"Content-Type": "application/json", "Content-Encoding": "gzip"},
    )
    return ({"status": "successfuly uploaded to storage"}, 200, {})


if not prod:
    from flask import Flask

    app = Flask(__name__)

    @app.route("/")
    def serve_get_pricelist():
        s = get_pricelist_json_out()
        return (
            s[0],
            s[1],
            s[2],
        )
