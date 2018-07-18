import requests


r = requests.post("http://127.0.0.1:8000/get_events", data={'file': 'request.json'})
#print(r.status_code, r.reason,r.text)
