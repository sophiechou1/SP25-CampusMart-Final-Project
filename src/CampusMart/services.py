import requests

GROUP = 'group14'
API_BASE_URL = f'https://jcssantos.pythonanywhere.com/api/{GROUP}/{GROUP}'

def get_access_token(username, password):
    response = requests.post(
        "https://jcssantos.pythonanywhere.com/api/token/",
        headers={"Content-Type": "application/json"},
        json={"username": username, "password": password},
    )
    if response.status_code == 200:     # check if given valid token response
        print("API response:", response.json())
        return response.json().get("access")
    else:
        raise Exception("Failed to get access token")
    
def view_all_coins(access_token):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   # Make a GET request with the authorization header
   api_response = requests.get("https://jcssantos.pythonanywhere.com/api/group14/group14/", headers=headers)
   if api_response.status_code == 200:
       # Process the data from the API
       print("API response:", api_response.json())
       return api_response.json()
   else:
       print("Failed to access the API endpoint to view all coins:", api_response.status_code)

def view_balance_for_user(access_token, email):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   # Make a GET request with the authorization header
   api_response = requests.get(f"https://jcssantos.pythonanywhere.com/api/group14/group14/player/{email}/", headers=headers)
   if api_response.status_code == 200:
       # Process the data from the API
       print("API response:", api_response.json())
       return api_response.json()['amount']
   else:
       print("Failed to access the API endpoint to view balance for user:", api_response.status_code)

def user_pay(access_token, email, amount):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   data = {"amount": amount} # non-negative integer value to be decreased
   # Make a POST request with the authorization header and data payload
   api_response = requests.post(f"https://jcssantos.pythonanywhere.com/api/group14/group14/player/{email}/pay", headers=headers, data=data)
   print("API response:", api_response.json())
   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to pay:", api_response.status_code)


# def view_user_balance(access_token, email):
#     print(f"Fetching balance from: {API_BASE_URL}/player/{email}/")
#     headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
#     response = requests.get(f"{API_BASE_URL}/player/{email}/", headers=headers)
#     if response.status_code == 200:
#         return response.json().get("amount")
#     else:
#         raise Exception(f"Failed to get user balance: {response.status_code}")

# def user_pay(access_token, email, amount):
#     headers = {'Authorization': f'Bearer {access_token}'}
#     data = {"amount": amount}
#     response = requests.post(f"{API_BASE_URL}/player/{email}/pay", headers=headers, data=data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise Exception(f"Failed to pay: {response.status_code} {response.text}")
