import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):

    @allure.description("AUTHENTICATE AND TRY TO DELETE WITH USER2")
    def test_auth_and_delete_user_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # Login
        response1 = MyRequests.post("/user/login", data=data)
        Assertions.assert_code_status(response1, 200)
        # Delete with authentication credentials
        response2 = MyRequests.delete("/user/2")
        Assertions.assert_code_status(response2, 200)
        print("\n The first 5 users can't be deleted")

    def test_create_user_successfully_and_delete_that_user(self):
        # Prepare registration data
        data = self.prepare_registration_data()

        # Create a new user
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        # Extract user credentials
        self.email = data['email']
        self.password = data['password']

        # Log in with the created user
        login_data = {'email': self.email, 'password': self.password}
        response3 = MyRequests.post("/user/login", data=login_data)
        Assertions.assert_code_status(response3, 200)

        # Extract authentication token and session ID
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # Delete with authentication credentials
        user_id = self.get_json_value(response, "id")
        delete_response = MyRequests.delete(f"/user/{user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(delete_response, 200)
        print("User authenticated with  own creds deleted successfully")

    def test_delete_a_user_with_another_user(self):
        # Prepare registration data for user1
        data1 = self.prepare_registration_data()

        # Create user1
        response1 = MyRequests.post("/user/", data=data1)
        response1_content = response1.content.decode('utf-8')
        print("\n User1 Creation Response Content:", response1_content)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_id = self.get_json_value(response1, "id")
        print("User1 ID:", user1_id)

        # Log in with user1
        login_data1 = {'email': data1['email'], 'password': data1['password']}
        response2 = MyRequests.post("/user/login", data=login_data1)
        Assertions.assert_code_status(response2, 200)

        # Extract authentication token and session ID for user1
        auth_sid1 = self.get_cookie(response2, "auth_sid")
        token1 = self.get_header(response2, "x-csrf-token")
        print(f"User1 auth_sid: {auth_sid1}, token: {token1}")

        # Prepare registration data for user2
        data2 = self.prepare_registration_data()

        # Create user2
        response3 = MyRequests.post("/user/", data=data2)
        response3_content = response3.content.decode('utf-8')
        print("User2 Creation Response Content:", response3_content)
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        user2_id = self.get_json_value(response3, "id")
        print("User2 ID:", user2_id)

        # Log in with user2
        login_data2 = {'email': data2['email'], 'password': data2['password']}
        response4 = MyRequests.post("/user/login", data=login_data2)
        Assertions.assert_code_status(response4, 200)

        # Extract authentication token and session ID for user2
        auth_sid2 = self.get_cookie(response4, "auth_sid")
        token2 = self.get_header(response4, "x-csrf-token")
        print(f"User2 auth_sid: {auth_sid2}, token: {token2}")

        # Ensure tokens and session IDs are correctly handled
        assert auth_sid1 != auth_sid2, "Auth SID for User1 and User2 should be different"
        assert token1 != token2, "Tokens for User1 and User2 should be different"

        # Attempt to delete user1 with user2's credentials
        response5 = MyRequests.delete(f"/user/{user1_id}",
                                      headers={"x-csrf-token": token2},
                                      cookies={"auth_sid": auth_sid2})
        response5_content = response5.content.decode('utf-8')
        print("Attempt to Delete User1 with User2's Credentials Response Content:", response5_content)
        print(f"Response Status Code: {response5.status_code}")
        print(f"Request Headers: {response5.request.headers}")
        print(f"Request Cookies: {response5.request._cookies}")
        print(f"Response Headers: {response5.headers}")
        print(f"Response Text: {response5.text}")

        # Assert the deletion is forbidden
        assert auth_sid1 != auth_sid2, "Auth SID for User1 and User2 should be different"
        assert token1 != token2, "Tokens for User1 and User2 should be different"

        Assertions.assert_code_status(response5, 200)
        print("User can be deleted successfully only if you authenticated with that user")

        # Log in with user1
        login_data1 = {'email': data1['email'], 'password': data1['password']}
        response9 = MyRequests.post("/user/login", data=login_data1)
        Assertions.assert_code_status(response9, 200)
        print("Attempt to Delete User1 with User2's Credentials Response Content:", response5_content)
        print(f"Response Status Code: {response9.status_code}")
        print(f"Request Headers: {response9.request.headers}")
        print(f"Request Cookies: {response9.request._cookies}")
        print(f"Response Headers: {response9.headers}")
        print(f"Response Text: {response9.text}")