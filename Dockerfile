# Get the Alpine Linux base image and Python 3.9
FROM python:3.9-alpine

# Environmental variables
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app \
    APP_PORT=5000

# The home directory of the app
WORKDIR $APP_HOME

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies of the app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copy the rest of the app code
COPY . .

# The volume of the app
VOLUME [ "$APP_HOME/data" ]

# Default port of the app
EXPOSE $APP_PORT

# Run the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
