from django.core.management.base import BaseCommand
from github.helper.DB import Update
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Update().all()
            self.stdout.write(self.style.SUCCESS("OK"))
        except Exception as e:
            print("Update Error:{}".format(e))
            traceback.print_exc()
