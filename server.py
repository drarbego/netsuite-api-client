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
        print("request headers ", req.headers)

    def on_post(self, req, resp):
        body = json.load(req.bounded_stream)

        json_response = netsuite_client.create_order(body)
        print("json response ", json_response)

app = falcon.API()

orders = OrdersResource()

app.add_route('/', orders)
