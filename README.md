# Restaurant Monitoring System

The Restaurant Monitoring System is a backend API that helps restaurant
owners track the online and offline status of their stores during
business hours. The system polls each store roughly every hour and
records whether the store was active or not in a CSV file. The system
also has data on the business hours of all the stores and the timezone
for each store.

The system provides two APIs:

1.  /trigger_report endpoint that triggers the generation of a report
    from the data provided (stored in the database). The API has no
    input and returns a report ID (a random string). The report ID is
    used to poll the status of report completion.

2.  /get_report endpoint that returns the status of the report or the
    CSV. The API takes a report ID as input and returns the following:

    -   If report generation is not complete, return "Running" as the
        output
    -   If report generation is complete, return "Complete" along with
        the CSV file with the following schema: store_id,
        uptime_last_hour(in minutes), uptime_last_day(in hours),
        update_last_week(in hours), downtime_last_hour(in minutes),
        downtime_last_day(in hours), downtime_last_week(in hours) The
        uptime and downtime reported in the CSV only include
        observations within business hours. The system extrapolates
        uptime and downtime based on the periodic polls we have ingested
        to the entire time interval.

## Data Sources 

The system has the following three sources of data:

1.  A CSV file with three columns (store_id, timestamp_utc, status)
    where status is active or inactive. All timestamps are in UTC.

2.  A CSV file with data on the business hours of all the stores. The
    schema of this data is store_id, dayOfWeek(0=Monday, 6=Sunday),
    start_time_local, end_time_local. These times are in the local time
    zone. If data is missing for a store, assume it is open 24\*7.

3.  A CSV file with data on the timezone for each store. The schema is
    store_id, timezone_str. If data is missing for a store, assume it is
    America/Chicago. This is used so that data sources 1 and 2 can be
    compared against each other.
    
**_NOTE:_**  Data files cannot be pushed due to lfs issue 
     
         #### Files structure 
         
         ```
            data/
            
              ├── business_hours.csv
              
              ├── stores.csv
              
              └── timezones.csv
            ```

## System Requirements 

* The data sources are not static, and the system
should not precompute the answers. The system should keep updating the
data every hour. 
* The system should store the CSVs into a relevant
database and make API calls to get the data.

## Installation 

To install the required packages, run the following command in the project directory:
```
    pipenv shell
    pip install -r requirements.txt

```

To install rabbitmq management docker server
```
    docker run -d --hostname my-rabbit --name restaurent-manager rabbitmq:3-management

```

To install postgresql docker

```

    docker run -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -v /postgresql/data:/var/lib/postgresql/data -d postgres:15

```

## Usage

Start postgres docker container in interactive mode

```

    docker exec -it 0c847b8babad -U postgres -p mysecretpassword

```

Create database and User in the container terminal
```

    psql
    CREATE DATABASE restaurant_poll
    CREATE USER poll_user WITH PASSWORD 'poll_password'
    ALTER USER poll_user WITH SUPERUSER
    GRANT ALL PRIVILEGES ON restaurant_poll TO 'poll_user'

```

Start rabbitmq:management server if container not running 

```

    docker ps -a
    docker run 'container ID'

```

Start Celery worker in a new terminal
```

    cd path/to/project_directory
    pipenv shell
    C_FORCE_ROOT=1 celery -A config worker -l info --purge -Q generate_report -P solo  -n config-1 

```

Make migrations in the Database

```

    python manage.py makemigrations 
    python manage.py migrate

```

To start the server, run the following command in the project directory:
```

    python manage.py runserver
    
```

The server will start running on http://localhost:8000

Note: Remember to add url prefix in the api like http://localhost:8000/api

## API Documentation

- ### /trigger_report

    This endpoint triggers the generation of a report from the data provided (stored in the database).

    * Request
    ```
    POST /api/trigger_report HTTP/1.1

    ```
    * Response
    ```
        HTTP/1.1 200 OK
    Content-Type: application/json

    {
        'message': 'Success', 
        'error_code':200,
        "report_id": "report slug"
    }

    ```

- ### /get_report

    This endpoint returns the status of the report or the CSV.
    
    * Request
    ```
    POST /api/get_report HTTP/1.1

    {
        report_id: "report slug"
    }

    ```
    * Response
    ```
        HTTP/1.1 200 OK
        Content-Type: text/csv

        [

            {
                store_id, 
                uptime_last_hour(in minutes), 
                uptime_last_day(in hours), 
                update_last_week(in hours), 
                downtime_last_hour(in minutes), 
                downtime_last_day(in hours), downtime_last_week(in hours)
            }
        
        ]


    ```

## Functionalities 

Used advance python features like -
 - RabbitMQ queue for generating report
 - Celery worker
 - Multithreading
 - Caching

