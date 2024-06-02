import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Authorisation cases")
@allure.title("Test Authentication")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Roman")
@allure.testcase("R-456")
class TestUserAuth(BaseCase):

        exclude_params = [
            ("no_cookie"),
            ("no_token")
        ]
        @allure.story('')
        def setup_method(self):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response1 = MyRequests.post("/user/login", data=data)
            print(response1.text)
            self.auth_sid = self.get_cookie(response1, "auth_sid")
            self.token = self.get_header(response1, "x-csrf-token")
            self.user_id_from_auth_method = self.get_json_value(response1, 'user_id')

        @allure.description("This tests that authorisation using the email and password is successful")
        def test_user_auth(self):
            with allure.step('Using the GET to log in'):
                response2 = MyRequests.get(
                    "/user/auth",
                    headers={"x-csrf-token": self.token},
                    cookies={"auth_sid": self.auth_sid}
                  )
            with allure.step('Do a check to confirm that the user_id is \n'
                             'corresponding with the user_id from setup_method'):
                Assertions.assert_json_value_by_name(
                    response2,
                    "user_id",
                    self.user_id_from_auth_method,
                    "User id from auth method is not equal to user id from Check method"

            )

        @allure.description("This test checks authorisation status without sending the token or auth cookie")
        @pytest.mark.parametrize('condition', exclude_params)
        def test_negative_auth_check(self, condition):
            with allure.step('Create a loop to check for token and cookies'):
                if condition == "no_cookie":
                    response2 = MyRequests.get(
                        "/user/auth",
                        headers={"x-csrf-token": self.token}
                    )
                else:
                    response2 = MyRequests.get(
                        "/user/auth",
                        cookies={"auth_sid": self.auth_sid}
                    )
            with allure.step('Check that the user_id value is 0 which which is expected for behaviour'):
                Assertions.assert_json_value_by_name(
                    response2,
                    "user_id",
                    0,
                    f"User is authorized with condition {condition}"
                )
