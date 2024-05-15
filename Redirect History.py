import requests

# Используем "get" тип запроса по указонному методу
response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

# Создаем цыкл подсчета редиректов и выводим финальный УРЛ
if response.history:
    print("Redirect count:", len(response.history))
    print("Final URL:", response.url)
else:
    print("No redirects")
