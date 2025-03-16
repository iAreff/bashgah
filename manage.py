# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys


# def main():
#     """Run administrative tasks."""
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bashgah.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()

try:
    from mysql.connector.django.base import DatabaseWrapper as ConnectorDatabaseWrapper
except ImportError:
    # اگر این مسیر موجود نباشد، احتمالاً از نسخه‌ای متفاوت استفاده می‌کنید
    ConnectorDatabaseWrapper = None

if ConnectorDatabaseWrapper is not None:
    @property
    def fixed_display_name(self):
        return self.settings_dict.get('NAME', '')
    ConnectorDatabaseWrapper.display_name = fixed_display_name

if __name__ == '__main__':
    import os, sys
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bashgah.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
