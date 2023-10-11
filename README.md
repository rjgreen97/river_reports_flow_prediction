# River Flow Predictions

![alt text](https://www.askaboutflyfishing.com/wp-content/uploads/2014/11/kelly-galloup.jpg)

## Order of Operations
1) **ForcastingSession** creates forecasts for all sites
2) **DatabaseWriter** updates `forecast` table

## Database Setup

psql -U rjgreen postgres

create table river reports
pg_dump -h jobs.riverreports.com -p 5432 -U rrdev -W -v -f riverreports.sql rrdev

psql -U rjgreen riverreports < riverreports.sql

psql -U rjgreen riverreports
