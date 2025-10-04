# Use the official Python image.
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8080 (Cloud Run expects this)
EXPOSE 8080

# Start the Django server
CMD gunicorn your_project_name.wsgi:application --bind 0.0.0.0:8080