# Use the official MS-SQL Server Docker image as a base
FROM mcr.microsoft.com/mssql/server:2019-latest

# Set environment variables
ENV MSSQL_SA_PASSWORD=YourPasswordHere
ENV ACCEPT_EULA=Y

# Create app directory
WORKDIR /app

# Copy SQL scripts to the container
COPY scripts/ /app/scripts/
USER root
# Set executable permissions for the initialization script
RUN chmod +x /app/scripts/initialize-db.sh

# Expose the port used by SQL Server
EXPOSE 1433

# Run initialization script when the container starts
CMD /bin/bash /app/scripts/initialize-db.sh
