import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature('User Get')
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("owner", "Roman")
@allure.testcase("R-3")
class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        with allure.step('Unauthenticated trying to get user with id=2 data : username and checking that the \n'
                         'response does not contain : email, firstName, lastName'):
            response = MyRequests.get("/user/2")
            Assertions.assert_json_has_key(response, 'username')
            Assertions.assert_json_has_no_key(response, 'email')
            Assertions.assert_json_has_no_key(response, 'firstName')
            Assertions.assert_json_has_no_key(response, 'lastName')

    def test_get_user_details_auth_as_same_user(self):
        with allure.step('Authenticated trying to get user with id=2 data : username, email, firstName, lastName'):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")

            response2 = MyRequests.get(
                f"/user/{user_id_from_auth_method}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            expected_fields = ['username', 'email', 'firstName', 'lastName']
            Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_other_user(self):
        with allure.step('Unauthenticated as user with id=2 trying to get user details with id=1 data checking that \n'
                         'username is returned  and checking that the response does not contain : email, firstName, '
                         'lastName'):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

            other_user_id = 1
            response2 = MyRequests.get(
                f"/user/{other_user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            response2 = MyRequests.get("/user/2")
            Assertions.assert_json_has_key(response2, 'username')
            Assertions.assert_json_has_no_key(response2, 'email')
            Assertions.assert_json_has_no_key(response2, 'firstName')
            Assertions.assert_json_has_no_key(response2, 'lastName')
