#!/bin/bash
set -e
set -x

# if running on sideshow, use the tunneling command below before this bin script:
#ssh -L 1111:localhost:5432 sideshow

 Database information
REMOTE_DB_HOST="jobs.riverreports.com"
REMOTE_DB_PORT="5432"
REMOTE_DB_NAME="postgres"
REMOTE_DB_USER="rrdev"

LOCAL_DB_NAME="riverreports"
LOCAL_DB_USER="rjgreen"

# Print current working directory
echo "Script is running as user: $(whoami)"
echo "Current working directory: $(pwd)"

echo "Dumping data from the remote database..."
pg_dump -h $REMOTE_DB_HOST -p $REMOTE_DB_PORT -U $REMOTE_DB_USER -d $REMOTE_DB_NAME -W > dump.sql

echo "Checking if local database exists..."
if psql -lqt | cut -d \| -f 1 | grep -qw $LOCAL_DB_NAME; then
  echo "Dropping the existing local database..."
  dropdb -U $LOCAL_DB_USER $LOCAL_DB_NAME
fi

echo "Creating a new local database..."
createdb -U $LOCAL_DB_USER $LOCAL_DB_NAME

echo "Loading data into the local database..."
psql -U $LOCAL_DB_USER -d $LOCAL_DB_NAME -w < dump.sql

echo "Cleaning up the dump file..."
rm dump.sql

echo "Data transfer complete!"
