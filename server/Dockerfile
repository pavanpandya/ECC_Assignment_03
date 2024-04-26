# Use an appropriate base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy server script and other necessary files
COPY server.py /app/server.py

# Create a directory for the server files
RUN mkdir /app/serverdata

# Expose the port specified as a command-line argument
EXPOSE 13101

# Define command to run the server script with specified port
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "13101"]
