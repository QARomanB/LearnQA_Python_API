import requests

def test_header_method():

    # Get the header from the response
    response = requests.get("https://playground.learnqa.ru/api/homework_header")
    headers = response.headers
    print("Response Headers:")
    for key, value in headers.items():
        print(f"{key}: {value}")

    # Get the header name and value and print it
    expected_header = 'x-secret-homework-header'
    expected_value = 'Some secret value'

   # Check if there are any cookies in the response
    assert len(headers) > 0, "No cookies received in the response"

   # Check if the name and value of the header are corresponding
    assert expected_header in headers, f"Header {expected_header} not found in the response"
    assert headers[expected_header] == expected_value, f"Expected header value '{expected_value}', but got '{headers[expected_header]}'"



