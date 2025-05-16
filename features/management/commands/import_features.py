import csv
from django.core.management.base import BaseCommand, CommandError
from features.models import Feature

class Command(BaseCommand):
    help = 'Import features from a CSV file into the Feature model'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing feature data'
        )

    def handle(self, *args, **options):
        path = options['csv_file']
        try:
            with open(path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    feature, created = Feature.objects.update_or_create(
                        name=row['name'],
                        feature_type=row['feature_type'],
                        latitude=float(row['latitude']),
                        longitude=float(row['longitude']),
                        defaults={
                            'size': float(row.get('size') or 0),
                            'description': row.get('description', '')
                        }
                    )
                    count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully imported/updated {count} features.'
                ))
        except FileNotFoundError:
            raise CommandError(f'File "{path}" does not exist')
        except KeyError as e:
            raise CommandError(f'Missing required column in CSV: {e}')
