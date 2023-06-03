import threading
import time
import functools
import pandas as pd
import pytz
from datetime import datetime, timedelta
from api.models import StoreStatus, BuissnessHour, TimeZone

@functools.lru_cache(maxsize=1, typed=False) # cache for 1 hour
def import_data():
    batch_size = 10000
   
    timezones_csv = pd.read_csv('data/timezone.csv', chunksize=batch_size)
    business_hours_csv = pd.read_csv('data/menu_hours.csv', chunksize=batch_size)
    stores_csv = pd.read_csv('data/store_status.csv', chunksize=batch_size)

    # Define timezone dictionary
    timezone_dict = {}
    for _, row in pd.concat(timezones_csv).iterrows():
        timezone_dict[row['store_id']] = pytz.timezone(row['timezone_str'])
        # timezone = TimeZone.objects.create(store_id=row['store_id'], timezone_str=row['timezone_str'])
    
    for business_hours_df in business_hours_csv:
        for i, row in business_hours_df.iterrows():
            start_time = pd.to_datetime(row['start_time_local']).time()
            end_time = pd.to_datetime(row['end_time_local']).time()
            business_hours = BuissnessHour.objects.create(store_id=row['store_id'], day_of_week=row['day'], start_time_local=start_time, end_time_local=end_time)
            

            
    # for stores_df in stores_csv:
    #     stores_df = stores_df.dropna(subset=['timestamp_utc'])
    #     stores_df['timestamp_utc'] = pd.to_datetime(stores_df['timestamp_utc'])

    #     for i, row in stores_df.iterrows():
    #         store_id = row['store_id']
    #         status = row['status']
    #         timezone = timezone_dict.get(store_id, pytz.timezone('America/Chicago'))
    #         timestamp_local = row['timestamp_utc'].astimezone(timezone)
    #         store = StoreStatus.objects.create(store_id=store_id,timestamp_utc=row['timestamp_utc'], status=status)


# run import_data() in a separate thread
def run_import_data():
    import_data()

# start the import_data() function in a separate thread
# t = threading.Thread(target=run_import_data)
# t.start()

# start a timer to refresh the cache every hour
def refresh_cache():
    while True:
        run_import_data()  # call the function to refill the cache
        time.sleep(7200)  # sleep for 1 hour

# start the refresh_cache() function in a separate thread
# t2 = threading.Thread(target=refresh_cache)
# t2.start()