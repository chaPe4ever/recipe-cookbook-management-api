from django.core.management.base import BaseCommand
from django.db import connection
from decouple import config


class Command(BaseCommand):
    help = "Create PostgreSQL schema if it doesn't exist (requires DB_SCHEMA env variable)"

    def handle(self, *args, **kwargs):
        db_schema = config("DB_SCHEMA", default=None)
        
        if not db_schema:
            self.stdout.write(
                self.style.WARNING(
                    "DB_SCHEMA environment variable is not set. Skipping schema creation."
                )
            )
            return

        # Check if we're using PostgreSQL
        db_engine = connection.settings_dict.get("ENGINE", "")
        if "postgresql" not in db_engine:
            self.stdout.write(
                self.style.WARNING(
                    f"Database engine is {db_engine}. Schema creation is only supported for PostgreSQL."
                )
            )
            return

        # Create schema if it doesn't exist
        with connection.cursor() as cursor:
            # Use IF NOT EXISTS to avoid errors if schema already exists
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{db_schema}";')
            self.stdout.write(
                self.style.SUCCESS(f'✓ Schema "{db_schema}" is ready (created or already exists)')
            )

