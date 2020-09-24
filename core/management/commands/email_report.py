import traceback
from django.core.management.base import BaseCommand
from emailreport.helper.fetch import Report
from emailreport.helper.format import ReportData
from emailreport.helper.send import Email
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:

            report = Report()
            process_report = ReportData()
            data = process_report.format(raw_report=report.getReport())
            emails = settings.EMAIL_REPORT_TO
            subject = f'Daily : Github Organisation Vulnerabilities Scan Report'
            Email(emails,subject,data)
            self.stdout.write(self.style.SUCCESS(
                "Email Sent to: {}".format(",".join(emails))))
        except Exception as e:
            print("Core Email Send Error:{}".format(e))
            traceback.print_exc()
