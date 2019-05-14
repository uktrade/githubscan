from gecko.helper.push import GeckoDataSet
from django.core.management.base import BaseCommand
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            report = GeckoDataSet()
            report.push()
            report.push_overview()
            self.stdout.write(self.style.SUCCESS("OK"))
        except Exception as e:
            print("Report Error:{}".format(e))
            traceback.print_exc()
