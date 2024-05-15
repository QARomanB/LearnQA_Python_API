import requests

# URL для отправки запросов
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# Функция для выполнения запросов без параметра method
def make_request_without_method(method):
    response = requests.request(method, url)
    print(f"HTTP-запрос {method} без параметра method:")
    print("Статус код:", response.status_code)
    print("Текст ответа:", response.text)
    print()

# 1. Делаем запрос всех типов без параметра method
for method in ['GET', 'POST', 'PUT', 'DELETE']:
    make_request_without_method(method)

# 2. Делаем запрос с неизвестными методами
for method in ['PATCH', 'HEAD', 'OPTIONS']:
    make_request_without_method(method)

# 3. Делаем запрос с правильным значением method для POST, GET, PUT, DELETE HTTP-методов
for method in ['POST', 'GET', 'PUT', 'DELETE']:
    payload = {'method': method}
    response = requests.request(method, url, params=payload)
    print(f"HTTP-запрос {method} с правильным значением method:")
    print("Статус код:", response.status_code)
    print("Текст ответа:", response.text)
    print()

# 4. Проверяем все возможные сочетания реальных типов запроса и значений параметра method
for method in ['GET', 'POST', 'PUT', 'DELETE']:
    for param_method in ['GET', 'POST', 'PUT', 'DELETE']:
        payload = {'method': param_method}
        response = requests.request(method, url, params=payload)
        if response.status_code == 200:
            if method != param_method:
                print("Несоответствие: Реальный метод запроса:", method, "| Значение параметра method:", param_method)
        else:
            if method == param_method:
                print("Несоответствие: Реальный метод запроса:", method, "| Значение параметра method:", param_method)
