import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounting.models import AthleteCourse

class Command(BaseCommand):
    help = 'کاربرانی که موعد شهریه آن‌ها در 3 روز آینده است'

    def handle(self, *args, **options):
        today = timezone.now().date()
        threshold = today + datetime.timedelta(days=3)  # به عنوان مثال، 7 روز آینده
        near_due_courses = []

        for ac in AthleteCourse.objects.all():
            due_date = ac.fee_due_date()
            # اگر تاریخ موعد در بازه امروز تا threshold باشد و پرداخت انجام نشده باشد
            if today <= due_date <= threshold and not ac.payment_status:
                near_due_courses.append(ac)

        if near_due_courses:
            self.stdout.write("ثبت‌نام‌هایی که موعد پرداخت آن‌ها نزدیک است:")
            for ac in near_due_courses:
                self.stdout.write(f"{ac} - موعد: {ac.fee_due_date()}")
        else:
            self.stdout.write("هیچ ثبت‌نامی با موعد پرداخت نزدیک یافت نشد.")