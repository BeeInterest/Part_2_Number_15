import sys
import requests
import time

print('Приложение ожидает запуска Flask')
time.sleep(30)


url = "http://127.0.0.1:5000"
try:
    number_students = sys.argv[1]
except:
    number_students = 20

url1 = f"{url}/create_table" 
url2 = f"{url}/fill_table/{number_students}"
url3 = f"{url}/young_old_student"

try:
    response1 = requests.get(url1)
    response1.raise_for_status()  

    data = response1.json()  
    print(data['message'])
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")


try:
    response2 = requests.get(url2)
    response2.raise_for_status()  

    data = response2.json()  
    print(data['message'])

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

try:
    response3 = requests.get(url3)
    response3.raise_for_status() 

    data = response3.json() 
    print(data['message'])

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")


