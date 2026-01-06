import requests

API_KEY = "2VdWoE5mPUkdwzdp9Il4wS8XuUgYXLB1"  
TELEPHONE = "237655586299"    

url = "https://gate.whapi.cloud/messages/text"

payload = {
    "to": TELEPHONE,
    "body": "Hello World! Test WhatsApp API ✅",
    "typing_time": 0
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

print("🚀 Test d'envoi WhatsApp...")

response = requests.post(url, json=payload, headers=headers)
print(f"Code: {response.status_code}")
print(f"Réponse: {response.text}")