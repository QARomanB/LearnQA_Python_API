import requests

def main():
    url = "https://playground.learnqa.ru/api/get_text"

    # отправка гет запроса
    response = requests.get(url)

    # проверка статус кода
    if response.status_code == 200:
        # выводд ответа !
        print("Response body:")
        print(response.text)
    else:
        print(f"Failed to get response. Status code: {response.status_code}")

if __name__ == "__main__":
    main()

