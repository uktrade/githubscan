import traceback
from django.core.management.base import BaseCommand
from emailreport.helper.fetch import Report
from emailreport.helper.format import ReportData
from emailreport.helper.send import Email
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            print()

            report = Report()
            process_report = ReportData()
            text = process_report.format(raw_report=report.getReport())

            for email in settings.EMAIL_REPORT_TO:
                Email(email, text)
                self.stdout.write(self.style.SUCCESS(
                    "Email Sent:{} OK".format(email)))
        except Exception as e:
            print("Core Email Send Error:{}".format(e))
            traceback.print_exc()
