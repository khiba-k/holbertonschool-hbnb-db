# Get the alpine linux base image and python3.9
FROM python:3.9-alpine

# Enviromental variables
ENV PYTHONUNBUFFERED=1\
    APP_HOME=app\
    APP_PORT=50000

#The home directory of the app
WORKDIR $APP_HOME

#Getting the Docker cache
COPY requirments.txt .

# Intall the dependancies of the app
RUN pip3 install --no-cache --virtual .build-deps gcc musl-dev \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

#Getting the rest of the app code
COPY . .

# The volume of the app
VOLUME [ "$APP_HOME/data" ]

#Default port of the app
EXPOSE $APP_PORT

#Run the app using Ginicorn
CMD ["sh", "-c", "gunicorn --bind 127.0.0.1:$APP_PORT wsgi.app"]