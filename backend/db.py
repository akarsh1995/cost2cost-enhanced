import os
from datetime import datetime
from random import random

from peewee import CharField, DateTimeField, IntegerField, Model, MySQLDatabase

connection_settings = dict(
    database=os.getenv("DATABASE"),
    host=os.getenv("HOST"),
    user=os.getenv("USERNAME"),
    passwd=os.getenv("PASSWORD"),
    ssl={"ca": "/etc/ssl/cert.pem"},
    charset="utf8mb4",
)


db = MySQLDatabase(**connection_settings)


class Product(Model):
    name = CharField()
    vendor = CharField()
    category = CharField()
    price = IntegerField()
    timestamp = DateTimeField()

    class Meta:
        database = db  # This model uses the "people.db" database.


if __name__ == "__main__":
    Product.create_table()
    products = [
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i3-10100 Desktop Processor 4 Cores up to 4.3GHz LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110100 ",
            "vendor": "amazon",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i3-10100F Desktop Processor 4 Cores up to 4.3GHz Without Processor Graphics LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110100F ",
            "vendor": "amazon",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i3-10105 Desktop Processor 4 Cores up to 4.4GHz LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110105 ",
            "vendor": "amazon",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i3-10105F Desktop Processor 4 Cores up to 4.4GHz Without Processor Graphics LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110105F ",
            "vendor": "amazon",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i5-10400 Desktop Processor 6 Cores up to 4.3GHz LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110400 ",
            "vendor": "mdcomp",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i5-10400F Desktop Processor 6 Cores up to 4.3GHz Without Processor Graphics LGA 1200 (Intel\u00ae 400 Series Chipset) 65W BX8070110400F ",
            "vendor": "vedanta",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
        {
            "name": "10th Gen Intel\u00ae Core\u2122 i7-10700F Desktop Processor 8 Cores up to 4.8GHz Without Processor Graphics LGA1200 (Intel\u00ae 400 Series chipset) 65W BX8070110700F ",
            "vendor": "vedanta",
            "category": "cpu",
            "price": 10000 + random() * 20000,
            "timestamp": datetime.now(),
        },
    ]
    for p in products:
        pr_id = Product.create(**p)
        print(pr_id)
