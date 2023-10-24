# RiverReports Flow Predictions

![alt text](https://flyrods.weebly.com/uploads/2/9/0/8/2908219/8020826_orig.jpg)

## Order of Operations
1) Use code found in **forecasting.sql** to create a `forecast` table
2) Set the database URL in `get_database_url()` found in **src/database_fetcher.py**
3) run `bin/forecasting_session` which will create a **ForcastingSession** object
4) The **ForcastingSession** object will create forecasts for all sites and write 7-day predictions to the `forecast` table

## Demo Database Setup

psql -U rjgreen postgres

create table river reports
pg_dump -h jobs.riverreports.com -p 5432 -U rrdev -W -v -f riverreports.sql rrdev

psql -U rjgreen riverreports < riverreports.sql

psql -U rjgreen riverreports
