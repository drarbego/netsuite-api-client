import json

import falcon

import config
from client import NetSuiteClient

netsuite_client = NetSuiteClient(
    config.NETSUITE_HOST,
    config.NETSUITE_SCRIPTS,
    config.NETSUITE_CREDENTIALS
)

class OrdersResource(object):
    def on_get(self, req, resp):
        page_size = req.params.get("page_size", 10)
        page_number = req.params.get("page_number", 0)

        json_response = netsuite_client.retrieve_orders(page_size, page_number)
        resp.body = json.dumps(json_response)
        print("json response ", json_response)

    def on_post(self, req, resp):
        body = json.load(req.bounded_stream)

        json_response = netsuite_client.create_order(body)
        print("json response ", json_response)

app = falcon.API()

orders = OrdersResource()

app.add_route('/', orders)
