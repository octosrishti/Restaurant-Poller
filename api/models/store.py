from django.db import models

class StoreStatus(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active"
        INACTIVE = "inactive"
    
    
    store_id= models.CharField(max_length=40,blank=False)
    timestamp_utc = models.DateTimeField(auto_now=True, blank=False)
    status = models.CharField(blank=False, max_length=10, choices=Status.choices, default=Status.ACTIVE)
    
    def __str__(self):
        return f'{self.store_id} - {self.timestamp_utc} - {self.status}'