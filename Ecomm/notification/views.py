from django.shortcuts import render

# Create your views here.
# First, install the necessary library:
# pip install pyfcm

# Import necessary modules
from pyfcm import FCMNotification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

# Initialize FCM with your server key
push_service = FCMNotification(api_key="AAAAhkj7a5w:APA91bGXnsbD6RKIH7oDQvwl_j8mGKAlT58mww6zuLwVHPws7XBhhCHezSzy6VTtVPku2r_f-NA7TVmstWMSnNs4Ixv_r_exR2wUzSGCCeCLjYLJ7EkNRz86Q6AwmHHUgwKvmH1DHOd6")


# Define a class-based view for sending notifications
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class SendNotificationAPI(View):
    @csrf_exempt
    def post(self, request):
        # Parse request body
        data = json.loads(request.body.decode('utf-8'))

        # Extract data from request
        registration_id = data.get('registration_id')
        title = data.get('title')
        message = data.get('message')

        # Send the notification
        if registration_id and title and message:
            result = self.send_notification(registration_id, title, message)
            return JsonResponse({"status": "success", "message": "Notification sent successfully.", "result": result})
        else:
            return JsonResponse({"status": "error", "message": "Missing parameters."}, status=400)

    @csrf_exempt
    def send_notification(self, registration_id, title, message):
        # Define the message payload
        message_payload = {
            "registration_ids": [registration_id],
            "data_message": {
                "title": title,
                "body": message
            }
        }

        # Send the notification
        result = push_service.notify_multiple_devices(**message_payload)

        return result
