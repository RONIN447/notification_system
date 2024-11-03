-> Notification System with FCM 

-> Overview
This project implements a Python-based solution for sending push notifications and in-app notifications to users.

-> Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <the directory name>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Firebase Cloud Messaging:
   - Create a Firebase project and obtain the server key.
   - Generate FCM tokens for mobile users.

4. Replace placeholder values in `notification_system.py`:
   - Update `YOUR_FCM_SERVER_KEY` with your actual Firebase server key.
   - Update `YOUR_FCM_TOKEN_FOR_*` with actual FCM tokens for your users.

5. Run the notification system:
   ```bash
   python notification_system.py
   ```
6. Run the server :
   -> python manage.py runserver
   
-> Additional Notes
- Ensure to handle FCM tokens securely.

Note:
As firebase has mitigated from FCM key to HTTPv1 , read the official firebase document to implement it .
