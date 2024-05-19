import requests

def test_cookie_method():

    # Get the cookies from the response
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    cookies = response.cookies



    # Get the cookie name and value and print it
    cookie_name = 'HomeWork'
    cookie_value = cookies.get(cookie_name)
    print(f"Value of '{cookie_name}' cookie:", cookie_value)

    # Check if there are any cookies in the response
    assert len(cookies) > 0, "No cookies received in the response"

    # Check if the expected cookie is present
    assert cookie_name in cookies.keys(), f"Expected cookie '{cookie_name}' is not present"

    # Check if the value of the cookie is correct
    expected_cookie_value = 'hw_value'
    assert cookie_value == expected_cookie_value, f"Cookie '{cookie_name}' has unexpected value: {cookie_value}"


