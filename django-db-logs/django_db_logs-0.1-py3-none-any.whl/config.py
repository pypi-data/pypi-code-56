from django.conf import settings

MSG_STYLE_SIMPLE = 'Simple'
MSG_STYLE_FULL = 'Full'

DJANGO_db_logs_ADMIN_LIST_PER_PAGE = getattr(settings, 'DJANGO_db_logs_ADMIN_LIST_PER_PAGE', 10)

DJANGO_db_logs_ENABLE_FORMATTER = getattr(settings, 'DJANGO_db_logs_ENABLE_FORMATTER', False)
