# Use an appropriate base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy client script and other necessary files
COPY client.py /app/client.py

# Create a directory for the client files
RUN mkdir /app/clientdata

# Define command to run the client script with specified host and port
CMD ["python", "client.py", "--host", "server", "--port", "13101"]