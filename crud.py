# running different commands

import copy
import uuid
from .models import Product, ProductScrapeEvent
from .db import get_session
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model

# session = get_session()    # declare our session
# sync_table(Product)
# sync_table(ProductScrapeEvent)


def create_entry(data:dict):
    return Product.create(**data)   # unpack data


def create_scrape_entry(data:dict):    # adding new items to a db
    data['uuid'] = uuid.uuid1() # includes a timestamp
    return ProductScrapeEvent.create(**data)


def add_scrape_event(data:dict, fresh=False):
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return product, scrape_obj