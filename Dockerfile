# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Set the default command to run when the container starts
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Expose port 8000 to allow external connections
EXPOSE 8000
