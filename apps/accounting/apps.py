from django.apps import AppConfig


class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounting'
    verbose_name= 'باشگاه ولیعصر (عج)'
    
    # def ready(self):
    #     from . import signals