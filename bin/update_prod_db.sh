#!/bin/bash

REMOTE_DB_HOST="jobs.riverreports.com"
REMOTE_DB_PORT="5432"
REMOTE_DB_NAME="postgres"
REMOTE_DB_USER="rrdev"

LOCAL_DB_NAME="riverreports"
LOCAL_DB_USER="rjgreen"
TABLE_NAME="rr.forecast"
PATH_TO_LOCAL_FORECAST_TABLE="/Users/rjgreen/forecast.sql"

# Dump forecast table locally
echo "Downloading forecast table..."
pg_dump -U LOCAL_DB_USER -d LOCAL_DB_NAME -t TABLE_NAME -f forecast.sql

# Move forecast table to production database
echo "Moving forecast table to production database..."
psql -U REMOTE_DB_USER -h REMOTE_DB_HOST -p REMOTE_DB_PORT -d REMOTE_DB_NAME -a -f PATH_TO_LOCAL_FORECAST_TABLE

# Clean up forecast file
rm forecast.sql

echo "Data transfer complete!"
