from django.core.management.base import BaseCommand
from FA01.models import Asset

class Command(BaseCommand):
    help = 'Check for assets nearing their preferred usage period and send notifications'

    def handle(self, *args, **options):
        assets = Asset.objects.filter(status='active')
        notified_count = 0

        for asset in assets:
            if asset.is_nearing_end_of_life():
                asset.send_end_of_life_notification()
                notified_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully checked {len(assets)} assets and sent {notified_count} notifications')
        ) 