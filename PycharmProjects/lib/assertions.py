import json
from requests import Response
class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):

        try:
            response_as_dict = response.json()
        except json.JSONDecoderError:
            assert False , f"The response is not in the JSON format. The response text is:{response.text}"

        assert name in response_as_dict, f"The JSON response doesn't have the key '{name}' "
        assert response_as_dict[name] == expected_value, error_message