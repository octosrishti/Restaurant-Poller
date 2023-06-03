from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from django.conf import settings
from .models import StoreStatus, Report, TimeZone, BuissnessHour
from django.template.defaultfilters import slugify
from api.utils import compute_uptime
from datetime import datetime
import json
import asyncio
from kombu import Connection


class GenerateReport(APIView):
    permission_classes = (permissions.AllowAny,)
    renderer_classes = [JSONRenderer]
    
    


    def get_report_status_from_db(self,report_id):
        report = Report.objects.get(report_id=report_id)
        if report is None:
            return None
        else:
            return report.status

    def get_report_data_from_db(self,report_id):
        """
        Retrieves the report data from the database for a given report_id.
        """
        print(report_id)
        report = Report.objects.get(report_id=report_id)

        if report is None:
            raise ValueError(f"No report found for report_id: {report_id}")

        return report.report
        
    
    def get(self, request):
        try:
            
            report = Report.objects.create(status="running")
            slug = str(slugify(report.id))
            report.report_id = slug
            report.save()
            # self.generate_report(slug)
            
            message = {
                "id": slug,
                "task":"api.tasks.generate_report",
                "kwargs":{
                    "report_id":slug
                }
            }
            
            with Connection(settings.BROKER_URL) as connection:
                queue = connection.SimpleQueue("generate_report")
                queue.put(message, serializer="json")
            
            return Response({
                "status":200,
                "message":"Creating Report",
                "report ID":slug
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(e)
            return Response({
                "status":500,
                "message":"cannot generate report"
            })
    
    def post(self,request, format=None):
        try:
            report_id = self.request.data["report_id"]
            report_status = self.get_report_status_from_db(report_id)
            
            if report_status is None:
                return Response({
                    "status":400,
                    "token":"Cannot fetch report with the given report ID"
                }, status=status.HTTP_400_BAD_REQUEST)
            elif report_status == "running":
                return Response({
                    "status":202,
                    "token":"Generating report in progress"
                }, status=status.HTTP_400_BAD_REQUEST)
            elif report_status == "completed":
                print("scasc")
                report_data = self.get_report_data_from_db(report_id)
                
                return Response({
                    "status":200,
                    "data":json.loads(report_data)
                }, status=status.HTTP_200_OK)
            
            
            
            return Response({
                "status":500,
                "token":"Internal server error"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as exc:
            print(exc)
            return Response({
                "status":400,
                "message":"cannot get report"
            },status=status.HTTP_400_BAD_REQUEST)
            

