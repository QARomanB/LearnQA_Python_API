import requests

def main():
    url = "https://playground.learnqa.ru/api/get_text"

    # Sending a GET request
    response = requests.get(url)

    # Checking the status code
    if response.status_code == 200:
        # Printing the response body
        print("Response body:")
        print(response.text)
    else:
        print(f"Failed to get response. Status code: {response.status_code}")

if __name__ == "__main__":
    main()

