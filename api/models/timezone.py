from django.db import models

class TimeZone(models.Model):

    store_id= models.CharField(max_length=40,blank=False)
    timezone_str = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return f'{self.store_id} - {self.timezone_str}'