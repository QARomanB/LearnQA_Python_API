from lib.my_requests import MyRequests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure
@allure.feature('Registration')
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Roman")
@allure.testcase("R-5")
class TestUserRegister(BaseCase):

    def test_create_user_successfully(self):
        with allure.step('preparing registration data for user'):

            data = self.prepare_registration_data()
        with allure.step('creating a user and checking the status code and  that user has id'):
            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        with allure.step('creating a user with existing email, checking the status code 400 and the error message'):
            email = 'vinkotov@example.com'
            data = self.prepare_registration_data(email)

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
                f"Unexpected response content: '{response.content}'"

    def test_create_user_with_incorrect_email(self):
        with allure.step('creating a user with incorrect  email, checking the status code 400 and the error message'):
            email = 'vinkotovexample.com'
            data = self.prepare_registration_data(email)

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "Invalid email format", \
                f"Unexpected response content: '{response.content}'"

    @pytest.mark.parametrize('missing_field', ['username', 'firstName', 'lastName', 'email', 'password'])
    def test_create_user_without_field(self, missing_field):
        with allure.step('creating a user  without any of the fields , checking the status code 400 and the error message'):
            data = self.prepare_registration_data()
            data.pop(missing_field)

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The following required params are missed: {missing_field}", \
                f"Unexpected response content: '{response.content}'"

    def test_create_user_with_short_name(self):
        with allure.step('Creating a user with  a 1 symbol name , checking the status code 400 and the error message'):
            data = self.prepare_registration_data()
            data['firstName'] = 'A'

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", \
                f"Unexpected response content: '{response.content}'"

    def test_create_user_with_long_name(self):
        with allure.step('Creating a user with  a 251 symbol name , checking the status code 400 and the error message'):
            data = self.prepare_registration_data()
            data['firstName'] = 'A' * 251

            response = MyRequests.post("/user/", data=data)

            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", \
                f"Unexpected response content: '{response.content}'"
