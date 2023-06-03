from django.urls import path, include
from .views import GenerateReport

urlpatterns = [
    path('trigger_report', GenerateReport.as_view()),
    path('get_report', GenerateReport.as_view())
]
