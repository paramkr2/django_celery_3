# Business Monitoring| Django + Celery

## Deployed Website: 
https://djangocelery2-production.up.railway.app/

##Environment Variables:
`
DEBUG
SECRET_KEY
DJANGO_ALLOWED_HOSTS
CELERY_BROKER
CELERY_BACKEND
DB_HOST
DB_PASSWORD
DB_PORT
`
## Two API endpoints 
    1. /trigger_report endpoint that will trigger report generation from the data provided (stored in DB)
        1. No input 
        2. Output - report_id (random string) 
        3. report_id will be used for polling the status of report completion
    2. /get_report endpoint that will return the status of the report or the csv
        1. Input - report_id
        2. Output
            - if report generation is not complete, return "Pending" as the output
            - if report generation is complete, return “Complete” along with the CSV file 


## Input Data Format:

We  have 3 sources of data 

1. Have data about whether the store was active or not in a CSV.  
The CSV has 3 columns (`store_id, timestamp_utc, status`) where status is active or inactive.  
All timestamps are in **UTC**
    
2. We have the business hours of all the stores - 
schema of this data is `store_id, dayOfWeek(0=Monday, 6=Sunday), start_time_local, end_time_local`
    1. These times are in the **local time zone**
    2. If data is missing for a store, assume it is open 24*7

3. Timezone for the stores - schema is `store_id, timezone_str`
    1. If data is missing for a store, assume it is America/Chicago

## Output Data Format:

A csv report  that has the following schema

`store_id, uptime_last_hour(in minutes), uptime_last_day(in hours), 
update_last_week(in hours), downtime_last_hour(in minutes), 
downtime_last_day(in hours), downtime_last_week(in hours)`

1. Uptime and downtime  only include observations within business hours. 
2. Extrapolated uptime and downtime based on the periodic polls available, to the entire time interval.
    1. eg, business hours for a store are 9 AM to 12 PM on Monday
        1. only have 2 observations for this store on a particular date (Monday) in our data at 10:14 AM and 11:15 AM
        2. need to fill the entire business hours interval with uptime and downtime from these 2 observations based on basic interpolation logic
