#!/bin/bash

# Make sure there are no active database session running!!!

# Database information
REMOTE_DB_HOST="jobs.riverreports.com"
REMOTE_DB_PORT="5432"
REMOTE_DB_NAME="postgres"
REMOTE_DB_USER="rrdev"

LOCAL_DB_NAME="riverreports"
LOCAL_DB_USER="rjgreen"

# Dump data from the remote database
echo "Dumping data from the remote database..."
pg_dump -h $REMOTE_DB_HOST -p $REMOTE_DB_PORT -U $REMOTE_DB_USER -d $REMOTE_DB_NAME -W > dump.sql

# # Drop the local database if it exists
if psql -lqt | cut -d \| -f 1 | grep -qw $LOCAL_DB_NAME; then
  echo "Dropping the existing local database..."
  dropdb -U $LOCAL_DB_USER $LOCAL_DB_NAME
fi

# # Create a new local database
echo "Creating a new local database..."
createdb -U $LOCAL_DB_USER $LOCAL_DB_NAME

# # Load data into the local database
echo "Loading data into the local database..."
psql -U $LOCAL_DB_USER -d $LOCAL_DB_NAME -w < dump.sql

# # Clean up the dump file
rm dump.sql

echo "Data transfer complete!"
