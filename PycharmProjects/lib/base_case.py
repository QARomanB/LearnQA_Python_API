import json.decoder

from requests import Response

class BaseCase:
    def get_cookie (self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with the name {cookie_name} in the last response"
        return response.cookies[cookie_name]


    def get_header (self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find the header with the name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value (self, response: Response, name):
        try :
            response_as_dict = response.json()
        except json.decoder.JSONDecoderError:
            assert False, f"Responce is not on the 'json' format, the response is in {response.text}"

        assert name in response_as_dict, f"The JSON response doesn't have the key {name}"
        return response_as_dict [name]
