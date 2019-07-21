from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client import prepare_upload
from django.conf import settings
import os
import csv


class Email:

    def __init__(self, emails, text):
        notifications_client = NotificationsAPIClient(settings.NOTIFY_API_KEY)

        FILE_NAME = 'report.csv'

        with open(FILE_NAME, 'w') as csvFile:
            f = csv.writer(csvFile)
            f.writerows(text)
            csvFile.close()

        for to in emails:
            with open(FILE_NAME, 'rb') as f:
                response = notifications_client.send_email_notification(
                    email_address=to,
                    template_id=settings.NOTIFY_TEMPLATE_ID,
                    personalisation={'link_to_document': prepare_upload(f)}
                )

        os.remove(FILE_NAME)
