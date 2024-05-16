import time
import requests
import json

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# Sending a GET request to the URL
response = requests.get(url)

# Checking the status code of the response
print("Status Code:", response.status_code)

# Printing the response text
print("Response Text:", response.text)

# Parsing the response text as JSON
data = json.loads(response.text)
# Extracting the token
token = data.get('token')
# Extract the time
seconds = data.get('seconds')

'''# Sending another GET request to the URL with a WRONG token as a parameter
response_with_token = requests.get(url, params={'token': '1348'})

# Print Code and text
print("Status Code:", response_with_token.status_code)
print("Response ERROR Text:", response_with_token.text)'''

# Sending another GET request to the URL with token as a parameter
response_with_token = requests.get(url, params={'token': token})

# Print Code and text
print("Status Code:", response_with_token.status_code)
print("Response Text:", response_with_token.text)

# Waiting for the time to elapse
time.sleep(seconds + 1)

# Sending another GET request to the URL with token as a parameter
response_with_token = requests.get(url, params={'token': token})

# Print Code and text
print("Status Code:", response_with_token.status_code)
print("Response Text:", response_with_token.text)