River Flow Predictions based on USGS/USBR Gage Data

psql -U rjgreen postgres
create table river reports
pg_dump -h jobs.riverreports.com -p 5432 -U rrdev -W -v -f riverreports.sql rrdev
psql -U rjgreen riverreports < riverreports.sql
psql -U rjgreen riverreports
