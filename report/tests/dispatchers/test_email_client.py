# -*- coding: utf-8 -*-
from pathlib import Path

from django.conf import settings

CSV_FILE_PATH = Path.joinpath(Path(__file__).parent, "fixtures", "test.csv")

receiver_email = "test1@dummy.com"
data = {
    "subject": "Testing: Email Dispatch",
    "content": "This is my december",
    "summary": "All is well",
}

temaplate_id = settings.GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID


def test_success_dispatcher(real_fast_test, fake_test_email_dispatcher):

    global receiver_email
    global data

    temaplate_id = settings.GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID

    try:
        fake_test_email_dispatcher.send_email_with_attachment(
            receiver_email=receiver_email,
            upload_file_path=CSV_FILE_PATH,
            data=data,
            notify_template_id=temaplate_id,
        )
        assert True
    except:
        assert False


def test_fail_dispatcher(real_fast_test, fake_test_email_dispatcher, caplog):

    global receiver_email
    global data
    temaplate_id = "This is no uuid"

    try:
        fake_test_email_dispatcher.send_email_with_attachment(
            receiver_email=receiver_email,
            upload_file_path=CSV_FILE_PATH,
            data=data,
            notify_template_id=temaplate_id,
        )
        assert False
    except:
        assert "Failed: Email delivery" in caplog.messages
        assert True
