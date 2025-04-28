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
        return response.json().get("access")
    else:
        raise Exception("Failed to get access token")

def view_user_balance(access_token, email):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f"{API_BASE_URL}/player/{email}/", headers=headers)
    if response.status_code == 200:
        return response.json().get("amount")
    else:
        raise Exception(f"Failed to get user balance: {response.status_code}")

def user_pay(access_token, email, amount):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {"amount": amount}
    response = requests.post(f"{API_BASE_URL}/player/{email}/pay", headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to pay: {response.status_code} {response.text}")
