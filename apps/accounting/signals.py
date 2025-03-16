import logging
from django.conf import settings
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
# from django.contrib.auth.models import Group, Permission
# from django.core.mail import send_mail


# @receiver(post_migrate)
# def create_groups(sender, **kwargs):
#     if sender.name == 'accounting':
#         admin_group, _ = Group.objects.get_or_create(name='Admin')
#         # coach_group, _ = Group.objects.get_or_create(name='Coach')
#         athlete_group, _ = Group.objects.get_or_create(name='Athlete')
        
#         admin_permissions = Permission.objects.all()
#         athlete_permissions = Permission.objects.none()
        
#         admin_group.permissions.set(admin_permissions)
#         athlete_group.permissions.set(athlete_permissions)


logger = logging.getLogger(__name__)

@receiver(post_save, sender=USER)
def check_insurance_date(sender, instance, created, **kwargs):
    # این سیگنال تنها در مواردی که رکورد به‌روزرسانی می‌شود اجرا می‌شود (نه هنگام ایجاد)
    if not created and instance.insurance_expiration_date is None:
        # ثبت لاگ هشدار
        logger.warning(f"کاربر {instance} بدون تاریخ انقضای بیمه ذخیره شده است.")
        
        # ارسال ایمیل هشدار به مدیر (آدرس ایمیل مدیر را در settings یا به صورت ثابت قرار دهید)
        send_mail(
            subject='هشدار: تاریخ انقضای بیمه وارد نشده',
            message=f'برای کاربر {instance} تاریخ انقضای بیمه وارد نشده است.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['admin@example.com'],  # آدرس‌های ایمیل مدیر یا تیم پشتیبانی
            fail_silently=False,)
        # در اینجا می‌توانید اقدامات دیگری مانند ایجاد یک اعلان در سیستم یا ثبت در پایگاه داده انجام دهید.
