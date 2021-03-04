from django.core.management.base import BaseCommand
import traceback
from github.db.updater import Updater
from github.client import GHClient


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            Updater().all()
            self.stdout.write(self.style.SUCCESS("OK"))
        except Exception as e:
            print("Github Fetch Error:{}".format(e))
            traceback.print_exc()
