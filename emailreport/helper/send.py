from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client import prepare_upload
from django.conf import settings
import os


class Email:

    def __init__(self, to, text):
        notifications_client = NotificationsAPIClient(settings.NOTIFY_API_KEY)

        f = open('report.txt', 'w+')
        f.write(text)
        f.closed
        print(to)
        with open('report.txt', 'rb') as f:
            response = notifications_client.send_email_notification(
                email_address=to,
                template_id=settings.NOTIFY_TEMPLATE_ID,
                personalisation={'link_to_document': prepare_upload(f)}
            )

        os.remove('report.txt')
