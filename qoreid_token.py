import requests
import json
from decouple import config

# # Endpoint URL
# url = "https://api.qoreid.com/token"

# # Headers
# headers = {
#     "accept": "text/plain",
#     "content-type": "application/json"
# }
# print(headers)
# data = {
#     "clientId": config('CLIENT_ID_KEY'),
#     "secret": config('CLIENT_SECRET_KEY')  
# }
# print(data)

# # Sending the POST request
# response = requests.post(url, headers=headers, json=data)
# print(response)

# # Checking the response
# if response.status_code == 201:  # 201 indicates success
#     token = response.json().get("token")  # Extract the token from the response
#     print("Response JSON:", response.json())

# else:
#     print("Failed to get token. Status Code:", response.status_code)
#     print("Response:", response.text)






# # Endpoint URL
# url = "https://api.qoreid.com/token"

# # Headers
# headers = {
#     "accept": "text/plain",
#     "content-type": "application/json"
# }

# # Payload
# data = {
#     "clientId": config('CLIENT_ID_KEY'),
#     "secret": config('CLIENT_SECRET_KEY')
# }

# # Sending the POST request
# response = requests.post(url, headers=headers, json=data)

# # Debugging and extracting the token
# if response.status_code == 201:  # Success
#     response_json = response.json()
#     token = response_json.get("accessToken")  # Updated to access 'accessToken'
#     if token:
#         print("Token:", token)
#     else:
#         print("Token not found in the response.")
# else:
#     print("Failed to get token. Status Code:", response.status_code)
#     print("Response:", response.text)



import requests

url = "https://api.qoreid.com/token"

headers = {
    "accept": "text/plain",
    "content-type": "application/json"
}

data = {
    "clientId": config('CLIENT_ID_KEY'),
    "secret": config('CLIENT_SECRET_KEY')
}

# response = requests.post(url, headers=headers)
response = requests.post(url, headers=headers, json=data)


print(response.text)