import requests

url = "https://yvonne-mahilum.onrender.com/skills"

try:
    response = requests.get(url, timeout=30)

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        print("Classmate's API Response:")
        print(data)

    else:
        print("Request failed.")
        print(response.text)

except requests.exceptions.RequestException as e:
    print("Connection error:", e)
