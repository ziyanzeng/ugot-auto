# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /ugot_auto

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port for the webpage service
EXPOSE 8000

# Define the command to run the application
CMD ["sh", "-c", "cd static && python -m http.server 8000 & cd /ugot_auto && python main.py"]