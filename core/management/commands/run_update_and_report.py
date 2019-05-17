from gecko.helper.push import GeckoDataSet
from django.core.management.base import BaseCommand
from github.helper.DB import Update
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Update().all()
            self.stdout.write(self.style.SUCCESS("GitHub Update: OK"))
        except Exception as e:
            print("Core Update Error:{}".format(e))
            traceback.print_exc()
        try:
            report = GeckoDataSet()
            report.push()
            report.push_overview()
            self.stdout.write(self.style.SUCCESS("Report Update: OK"))
        except Exception as e:
            print("Core Report Error:{}".format(e))
            traceback.print_exc()
