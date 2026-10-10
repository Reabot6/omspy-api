"""
* Production code from (SFG) | seofg.xyz
* Built by Reabot6 | github.com/reabot6
*
* This file is part of the omspy-api open source release.
* Licensed under the MIT License.
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand


class TestDataCommand(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--reset_db",
            action="store_true",
            help="Drop and recreate all DB tables before inserting.",
        )

    def handle(self, *args, **options):
        if options["reset_db"]:
            call_command("reset_db", "--noinput")
            call_command("migrate")
        self.insert_data()

    def insert_data(self):
        raise NotImplementedError("Subclasses must implement insert_data().")
