import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounting.models import USER

class Command(BaseCommand):
    help = 'بررسی کاربرانی که تاریخ انقضای بیمه آن‌ها در 10 روز آینده است.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        threshold = today + datetime.timedelta(days=10)
        expiring_users = USER.objects.filter(
            insurance_expiration_date__gte=today,
            insurance_expiration_date__lte=threshold
        )

        if expiring_users.exists():
            self.stdout.write("کاربرانی با تاریخ انقضای بیمه نزدیک:")
            for user in expiring_users:
                self.stdout.write(f"کاربر: {user}, تاریخ انقضا: {user.insurance_expiration_date}")
        else:
            self.stdout.write("هیچ کاربری با تاریخ انقضای بیمه نزدیک یافت نشد.")