import json

json_data = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

parsed_data = json.loads(json_data)

second_message_text = parsed_data['messages'][1]['message']
print(second_message_text)