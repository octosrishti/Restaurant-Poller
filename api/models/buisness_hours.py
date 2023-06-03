from django.db import models

class BuissnessHour(models.Model):

    store_id= models.CharField(max_length=40,blank=False)
    day_of_week= models.IntegerField(blank=False)
    start_time_local = models.TimeField(auto_now=False, blank=False)
    end_time_local = models.TimeField(auto_now=False, blank=False)
    
    def __str__(self):
        return f'{self.store_id} - {self.day_of_week} - {self.start_time_local} - {self.end_time_local}'