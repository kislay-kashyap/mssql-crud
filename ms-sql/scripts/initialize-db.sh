#!/bin/bash

# Start the SQL Server
/opt/mssql/bin/sqlservr &

# Wait for SQL Server to start
sleep 20s

# Run SQL scripts to create the database and table
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourPasswordHere -d master -i /app/scripts/create-db.sql

# Keep the container running
tail -f /dev/null
