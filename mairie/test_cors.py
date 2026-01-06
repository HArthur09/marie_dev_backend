# backend/mairie/test_cors.py
import requests
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def test_cors():
        """Teste la configuration CORS"""
        
        # Test avec ngrok (remplacez par votre URL)
        ngrok_url = "https://jessie-tangled-unlethargically.ngrok-free.dev"
        
        # Test 1: Options preflight request
        print("🔍 Test 1: Preflight request (OPTIONS)")
        try:
            response = requests.options(
                f"{ngrok_url}/api/login/",
                headers={
                    'Origin': ngrok_url,
                    'Access-Control-Request-Method': 'POST',
                    'Access-Control-Request-Headers': 'Content-Type',
                }
            )
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Test 2: GET request
        print("\n🔍 Test 2: GET request")
        try:
            response = requests.get(
                f"{ngrok_url}/api/csrf/",
                headers={'Origin': ngrok_url}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Cookies reçus: {response.cookies}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
        
        # Test 3: Login request
        print("\n🔍 Test 3: Login request")
        try:
            # D'abord récupérer le CSRF token
            csrf_response = requests.get(f"{ngrok_url}/api/csrf/")
            csrf_token = csrf_response.cookies.get('csrftoken')
            
            # Ensuite login
            login_response = requests.post(
                f"{ngrok_url}/api/login/",
                json={"username": "admin", "password": "demo123"},
                headers={
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf_token if csrf_token else '',
                    'Origin': ngrok_url,
                },
                cookies=csrf_response.cookies
            )
            print(f"   Status: {login_response.status_code}")
            print(f"   Réponse: {login_response.text}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")

    if __name__ == "__main__":
        test_cors()