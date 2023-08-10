# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory to /app
WORKDIR /app

# Import the GPG keys for Microsoft repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Add the Microsoft repository to apt sources
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable for Flask
ENV FLASK_ENV=development

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
