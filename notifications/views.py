import json
import requests
import logging
from datetime import datetime
from django.http import JsonResponse
from google.oauth2 import service_account 
from google.auth.transport.requests import Request

from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Notification System with FCM !")

# configuring the loggingg 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# the user data simulation of 5 users 
users = [
    {"userID": 1, "name": "Alice", "device_type": "mobile", "fcm_token": "YOUR_FCM_TOKEN_FOR_ALICE"},
    {"userID": 2, "name": "Bob", "device_type": "web"},
    {"userID": 3, "name": "Charlie", "device_type": "mobile", "fcm_token": "YOUR_FCM_TOKEN_FOR_CHARLIE"},
    {"userID": 4, "name": "Diana", "device_type": "web"},
    {"userID": 5, "name": "Eve", "device_type": "mobile", "fcm_token": "YOUR_FCM_TOKEN_FOR_EVE"},
]

# As firebase has migrated from FCM Api to HTTP v1 
# we need to store a json file of the confidential details in the folder of the project 
# this is the path of that jspon file in my desktop 
SERVICE_ACCOUNT_FILE = r'C:\Users\aksha\notifcation_assignment\notification_system\notification-7b181-firebase-adminsdk-bqzr4-1c5d2745d0.json'

def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )
    # Refreshing the credentials to get a new access token
    credentials.refresh(Request())
    return credentials.token

# sending the notifications 

def send_push_notification(user, title, message):
    access_token = get_access_token()
    url = 'https://fcm.googleapis.com/v1/projects/notification-7b181/messages:send'
    
    payload = {
        'message': {
            'token': user['fcm_token'],
            'notification': {
                'title': title,
                'body': message,
                'timestamp': datetime.now().isoformat(),
                'type': 'Push'
            }
        }
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    

    # try and catching the responses and the errors 
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info(f"Push notification sent to {user['name']} (ID: {user['userID']}) - Status: Success")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send push notification to {user['name']} (ID: {user['userID']}) - Error: {e}")

def send_in_app_notification(user, title, message):
    logging.info(f"In-App notification sent to {user['name']} (ID: {user['userID']}) - Title: {title}, Message: {message}, Type: In-App")

def send_notification(users, title, message):
    for user in users:
        if user['device_type'] == 'mobile' and 'fcm_token' in user:
            send_push_notification(user, title, message)
        elif user['device_type'] == 'web':
            send_in_app_notification(user, title, message)
        else:
            logging.warning(f"Invalid device type for user {user['name']} (ID: {user['userID']})")

def send_notification_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        send_notification(users, title, message)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})