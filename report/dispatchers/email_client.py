# -*- coding: utf-8 -*-
from notifications_python_client import prepare_upload
from notifications_python_client.notifications import NotificationsAPIClient
from django.conf import settings
from common.functions import isinstance_of
from pathlib import PosixPath

import logging

logger = logging.getLogger(__name__)


class EmailClient:
    def __init__(self, api_key=settings.GOV_NOTIFY_API_KEY):
        self.client = self.email_client = NotificationsAPIClient(api_key)

    def send_email_with_attachment(
        self, receiver_email, uplod_file_path, data, notify_template_id
    ):
        try:
            isinstance_of(uplod_file_path, PosixPath, "uplod_file_path")

            isinstance_of(data, dict, "data")

            with open(uplod_file_path, "rb") as f:
                upload_file = prepare_upload(f, is_csv=True)

            personalisation_data = {
                "subject": f"{data['subject']}",
                "content": f"{data['content']}",
                "summary": f"{data['summary']}",
                "report": upload_file,
                "signature": settings.EMAIL_SIGNATURE,
            }

            response = self.client.send_email_notification(
                email_address=receiver_email,
                template_id=notify_template_id,
                personalisation=personalisation_data,
            )
        except:
            logger.info("Failed: Email delivery")
            raise

    def send_email(self, receiver_email, data, notify_template_id):
        """
        Not tested!
        """
        try:
            isinstance_of(data, dict, "data")

            personalisation_data = {
                "subject": f"{data['subject']}",
                "content": f"{data['content']}",
                "signature": settings.EMAIL_SIGNATURE,
            }

            response = self.client.send_email_notification(
                email_address=receiver_email,
                template_id=notify_template_id,
                personalisation=personalisation_data,
            )
        except:
            logger.info("Failed: Email delivery")
            raise
