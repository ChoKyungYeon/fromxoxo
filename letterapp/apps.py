from django.apps import AppConfig
class LetterappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'letterapp'
    verbose_name = '편지 정보'

    def ready(self):
        import letterapp.signals