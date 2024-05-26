import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content: '{response.content}'"

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", \
            f"Unexpected response content: '{response.content}'"

    @pytest.mark.parametrize('missing_field', ['username', 'firstName', 'lastName', 'email', 'password'])
    def test_create_user_without_field(self, missing_field):
        data = self.prepare_registration_data()
        data.pop(missing_field)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
            f"Unexpected response content: '{response.content}'"

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'K'

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", \
            f"Unexpected response content: '{response.content}'"

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['firstName'] = 'Z' * 251

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", \
            f"Unexpected response content: '{response.content}'"
