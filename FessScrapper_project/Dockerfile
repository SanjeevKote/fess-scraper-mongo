# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# # Install system dependencies
# RUN apt-get update \
#     && apt-get install -y netcat

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Django service is running on port 8000
EXPOSE 8000

# # Start the Django app
# CMD ["./start.sh"]

# RUN apt-get update && apt-get install -y netcat && apt-get clean
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]