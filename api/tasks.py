from celery import shared_task
import time
import json
from api.models import StoreStatus, Report
from api.utils import compute_uptime

@shared_task(max_retries=10, default_retry_delay=10)
def generate_report(report_id):
    """shared task consumig queue and generating report

    Args:
        report_id (_type_): _description_
    """
    
    #  Create new report object and add it to the database
 
    print("generating report", report_id)
    
    report = Report.objects.get(pk=report_id)
    
    # # Generate report data
    report_data = []
    stores = StoreStatus.objects.all()
    for store in stores[:10]:
        uptime_in_day, uptime_in_hour, uptime_in_week, downtime_in_day, downtime_in_hour, downtime_in_week = compute_uptime(store.store_id)
        report_data.append({
            'store_id': store.store_id,
            'status': store.status,
            'uptime_in_day': round(uptime_in_day, 2),
            'uptime_in_hour': round(uptime_in_hour, 2),
            'uptime_in_week': round(uptime_in_week, 2),
            'downtime_in_day': round(downtime_in_day, 2),
            'downtime_in_hour': round(downtime_in_hour, 2),
            'downtime_in_week': round(downtime_in_week, 2)
        })

    # # Update report object with status and completed_at
    report.status = 'completed'

    # # Update report data object with generated report data
    report.report = json.dumps(report_data)

    report.save()

    
