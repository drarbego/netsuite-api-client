import json
import logging

import requests
from requests_oauthlib import OAuth1

REQUEST_LIMIT_EXCEEDED_CODE = 'SSS_REQUEST_LIMIT_EXCEEDED'
MAX_NS_RETRIES = 10


class NetSuiteClientError(Exception):
    def __init__(self, response):
        self._response = response

    def __str__(self):
        return self._response.text


class TooManyRetriesError(Exception):
    def __init__(self, method, script_data):
        self._method = method
        self._script_id = script_data['id']
        self._deploy = script_data['deploy']

    def __str__(self):
        return f'Too many retries to call {self.method} '''\
            '''on script {self._script_id} (deploy: {self._deploy}). '''\
            '''Giving up.'''


class NetSuiteClient:
    def __init__(self, host, scripts, credentials):
        self._host = host
        self._scripts = scripts
        self._credentials = credentials

    def create_order(self, order_data):
        response = self._post(self._scripts["orders"], json=order_data)

        self._handle_errors(response)

        return response.json()

    def retrieve_order(self, order_id):
        response = self._get(self._scripts["orders"], params={ "order_id": order_id })

        self._handle_errors(response)

        return response.json()


    def _get(self, script_data, retries=MAX_NS_RETRIES, **kwargs):
        return self._make_request('get', script_data, retries, **kwargs)

    def _post(self, script_data, retries=MAX_NS_RETRIES, **kwargs):
        return self._make_request('post', script_data, retries, **kwargs)

    def _put(self, script_data, retries=MAX_NS_RETRIES, **kwargs):
        return self._make_request('put', script_data, retries, **kwargs)

    def _delete(self, script_data, retries=MAX_NS_RETRIES, **kwargs):
        return self._make_request('delete', script_data, retries, **kwargs)

    def _make_request(self, method, script_data, retries=MAX_NS_RETRIES, **kwargs):
        url = self._get_url(script_data)
        auth = self._get_auth(self._credentials)
        headers = self._get_headers()

        response = requests.request(method, url, auth=auth, headers=headers, **kwargs)

        if self._contains_request_limit_error(response):
            if retries:
                logging.info('%s request limit exceeded, retries left: %i', method, retries)
                return self._make_request(method, script_data, retries - 1, **kwargs)
            else:
                raise TooManyRetriesError(method, script_data)

        return response

    def _contains_request_limit_error(self, response):
        if response.status_code != 400:
            return False

        json = response.json()
        if type(json) is not dict:
            return False

        error_code = json.get('error', {}).get('code')

        return error_code == REQUEST_LIMIT_EXCEEDED_CODE

    def _get_url(self, script_data):
        script_id = script_data["id"]
        script_deploy = script_data["deploy"]

        return f"{self._host}/app/site/hosting/restlet.nl?script={script_id}&deploy={script_deploy}"

    def _get_auth(self, credentials):
        return OAuth1(
            credentials["consumer_key"],
            credentials["consumer_secret"],
            credentials["token_key"],
            credentials["token_secret"],
            realm=credentials["realm"],
        )

    def _get_headers(self):
        return {"Content-Type": "application/json"}

    def _handle_errors(self, response):
        if response.status_code != requests.codes.ok:
            raise NetSuiteClientError(response)

