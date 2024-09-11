# -*- coding: utf-8 -*-

import logging
from pathlib import PosixPath

from django.conf import settings
from notifications_python_client import prepare_upload
from notifications_python_client.notifications import NotificationsAPIClient

from common.functions import isinstance_of

logger = logging.getLogger(__name__)


class EmailClient:
    def __init__(self, api_key=settings.GOV_NOTIFY_API_KEY):
        self.client = self.email_client = NotificationsAPIClient(api_key)

    def send_email_with_attachment(
        self, receiver_email, upload_file_path, data, notify_template_id
    ):
        try:
            isinstance_of(upload_file_path, PosixPath, "upload_file_path")

            isinstance_of(data, dict, "data")

            with open(upload_file_path, "rb") as f:
                upload_file = prepare_upload(
                    f, retention_period="2 weeks", confirm_email_before_download=False
                )

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
