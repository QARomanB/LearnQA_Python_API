import requests


def main():
    url = "https://playground.learnqa.ru/api/get_text"

    # Otpravka get zaprosa
    response = requests.get(url)

    # Vivod Tela otveta
    print("Response body:")
    print(response.text)


if __name__ == "__main__":
    main()
