from django.apps import AppConfig
import threading
import django 
from django.conf import settings

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    
    def ready(self):
        pass
        from .service import run_import_data
        from api.service import refresh_cache
     
        t = threading.Thread(target=refresh_cache)
        t.start()