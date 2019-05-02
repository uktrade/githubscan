from gecko.helper.push import GeckoDataSet
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            report = GeckoDataSet()
            report.push()
            report.push_overview()
            self.stdout.write(self.style.SUCCESS("OK"))
        except Exception as err:
            print(err)
