from django.db import models

class Report(models.Model):

    class Status(models.TextChoices):
        RUNNING = "running"
        COMPLETED = "completed"
    
    
    report_id= models.CharField(blank=True, max_length=100)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.RUNNING)
    report = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.report_id} - {self.status}'