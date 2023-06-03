from .models import StoreStatus, BuissnessHour, TimeZone
from datetime import datetime, time, timedelta
import pytz
from django.utils.timezone import make_aware

def compute_uptime(store_id):
    start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date_hours = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(hours=1)
    end_date_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    end_date_weeks = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(weeks=1)
 
    timezone =  get_store_timezone(store_id)
    business_hours = get_store_business_hours(store_id)
    minutes_open = compute_business_hours_overlap(business_hours, timezone, start_date, end_date_hours, 60)
    hours_open_days = compute_business_hours_overlap(business_hours, timezone, start_date, end_date_day, 3600)
    hours_open_weeks = compute_business_hours_overlap(business_hours, timezone, start_date, end_date_weeks, 3600)
    
    uptime_in_hour = minutes_open / timedelta(minutes=60) * 100
    uptime_in_day = hours_open_days / timedelta(hours=24) * 100
    uptime_in_week = hours_open_weeks / timedelta(hours=24) * 100
    
    downtime_in_hour = 100 - uptime_in_hour
    downtime_in_day = 100 - uptime_in_day
    downtime_in_week = 100 - uptime_in_week
    return uptime_in_day, uptime_in_hour, uptime_in_week, downtime_in_day, downtime_in_hour, downtime_in_week

def get_store_timezone(store_id):
    timezone = TimeZone.objects.filter(store_id=store_id)
    if timezone is None or len(timezone)==0:
        # Return a default timezone here, e.g. UTC
        return pytz.timezone('UTC')
    return pytz.timezone(timezone[0].timezone_str)


def get_store_business_hours(store_id):
    
    business_hours = BuissnessHour.objects.filter(store_id=store_id)
    return [(bh.day_of_week, bh.start_time_local, bh.end_time_local) for bh in business_hours]


def compute_business_hours_overlap(business_hours, timezone, start_date, end_date, format):
    total_overlap = timedelta()
    
    # timezone = pytz.timezone(timezone)
    for day, start_time, end_time in business_hours:
        start_time_utc = timezone.localize(datetime.combine(start_date.date(), start_time)).astimezone(pytz.utc)
        end_time_utc = timezone.localize(datetime.combine(end_date.date(), end_time)).astimezone(pytz.utc)
        if start_time_utc >= end_time_utc:
            end_time_utc += timedelta(days=1)
        business_day_start = max(make_aware(start_date), start_time_utc)
        business_day_end = min(make_aware(end_date), end_time_utc)
        
        
        overlap = (business_day_end - business_day_start).total_seconds() / format 
        overlap = max(overlap, 0)
        total_overlap += timedelta(hours=overlap)
    return total_overlap