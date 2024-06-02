import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.feature('User Edition')
@allure.severity(allure.severity_level.MINOR)
@allure.label("owner", "Roman")
@allure.testcase("R-3")
class TestUserEdit(BaseCase):
    user_data_1 = None
    user_data_2 = None


    @classmethod
    def setup_class(cls):
        base_case_instance = BaseCase()

        # REGISTRATION of first user if not already done
        with allure.step('Registration of user1'):
            if cls.user_data_1 is None:
                register_data_1 = base_case_instance.prepare_registration_data()
                response1 = MyRequests.post("/user/", data=register_data_1)
                Assertions.assert_code_status(response1, 200)
                Assertions.assert_json_has_key(response1, "id")

                cls.user_data_1 = {
                    "email": register_data_1['email'],
                    "password": register_data_1['password'],
                    "user_id": base_case_instance.get_json_value(response1, "id")
                }

        # REGISTRATION of second user if not already done
        with allure.step('Registration of user2'):
            if cls.user_data_2 is None:
                register_data_2 = base_case_instance.prepare_registration_data()
                response2 = MyRequests.post("/user/", data=register_data_2)
                Assertions.assert_code_status(response2, 200)
                Assertions.assert_json_has_key(response2, "id")

                cls.user_data_2 = {
                    "email": register_data_2['email'],
                    "password": register_data_2['password'],
                    "user_id": base_case_instance.get_json_value(response2, "id")
                }


    def test_edit_just_created_user(self):
        # LOGIN
        with allure.step('Loging in with user1'):
            login_data = {
                'email': self.user_data_1['email'],
                'password': self.user_data_1['password']
            }
            response2 = MyRequests.post("/user/login", data=login_data)

        with allure.step('Storing token and auth_sid in variables '):
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step('Editing the user1 name and checking for status code 200'):
            new_name = "Changed name"

            response3 = MyRequests.put(
                f"/user/{self.user_data_1['user_id']}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step('Getting the user firstName and comparing with the new_name variable  '):
            response4 = MyRequests.get(
                f"/user/{self.user_data_1['user_id']}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

    def test_edit_user_while_unauthorized(self):
        # EDIT without authorization
        with allure.step('Editing the user1 name while unauthorised; checking for status code 400 and error messages'):
            new_name = "Changed name"

            response2 = MyRequests.put(
                f"/user/{self.user_data_1['user_id']}",
                data={"firstName": new_name}
            )

            Assertions.assert_code_status(response2, 400)
            assert 'error' in response2.json(), "There is no 'error' key in the response"
            assert response2.json()['error'] == "Auth token not supplied", \
                f"Unexpected response content: {response2.content.decode('utf-8')}"

    def test_edit_user_as_another_user(self):

        # LOGIN as second user
        with allure.step('Loging in with user2'):
            login_data_2 = {
                'email': self.user_data_2['email'],
                'password': self.user_data_2['password']
            }
            response3 = MyRequests.post("/user/login", data=login_data_2)
        with allure.step('Storing token_2 and auth_sid_2 as variables '):
            auth_sid_2 = self.get_cookie(response3, "auth_sid")
            token_2 = self.get_header(response3, "x-csrf-token")

        # Attempt to EDIT first user as second user
        with allure.step('Trying to edit user1 while logged in user2'):
            new_name = "Changed name"

            response4 = MyRequests.put(
                f"/user/{self.user_data_1['user_id']}",
                headers={"x-csrf-token": token_2},
                cookies={"auth_sid": auth_sid_2},
                data={"firstName": new_name}
            )

        # Assert that the request is forbidden or results in an error
        with allure.step('Checking for status code, and error messages'):
            Assertions.assert_code_status(response4, 400)
            assert 'error' in response4.json(), "There is no 'error' key in the response"
            assert response4.json()['error'] in [
                "Auth token not supplied",
                "You don't have permission to perform this action",
                "This user can only edit their own data."
            ], f"Unexpected response content: {response4.content.decode('utf-8')}"

    def test_edit_user_with_invalid_email(self):

        # LOGIN
        with allure.step('Loging in with user1'):
            login_data = {
                'email': self.user_data_1['email'],
                'password': self.user_data_1['password']
            }
            response2 = MyRequests.post("/user/login", data=login_data)

        with allure.step('Storing token and auth_sid as variables '):
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT email to invalid email
        with allure.step('Trying to edit user email to an invalid email'):
            invalid_email = "vinkotovexample.com"

            response3 = MyRequests.put(
                f"/user/{self.user_data_1['user_id']}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"email": invalid_email}
            )
        with allure.step('Checking for status code, and error messages'):
            Assertions.assert_code_status(response3, 400)
            assert 'error' in response3.json(), "There is no 'error' key in the response"
            assert response3.json()['error'] == "Invalid email format", \
                f"Unexpected response content: {response3.content.decode('utf-8')}"

    def test_edit_user_with_short_first_name(self):
        # LOGIN
        with allure.step('Loging in with user1'):
            login_data = {
                'email': self.user_data_1['email'],
                'password': self.user_data_1['password']
            }
            response2 = MyRequests.post("/user/login", data=login_data)

        with allure.step('Storing token and auth_sid as variables '):
            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT firstName to a short value of 1 symbol
        with allure.step('Trying to edit the firstName to a new one containing only one symbol'):
            short_first_name = "K"

            response3 = MyRequests.put(
                f"/user/{self.user_data_1['user_id']}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": short_first_name}
            )
        with allure.step('Checking for status code, and error messages'):
            Assertions.assert_code_status(response3, 400)
            assert 'error' in response3.json(), "There is no 'error' key in the response"
            assert response3.json()['error'] == "The value for field `firstName` is too short", \
                f"Unexpected response content: {response3.content.decode('utf-8')}"
