Holbertonschool-hbnb-db
Overview
This project is a Python web application deployed using Docker. It leverages SQLAlchemy for database management and JWT for authentication.

Features
Alpine Linux base image for lightweight Docker containers
Python 3.9 environment
Dependency management via requirements.txt
SQLAlchemy ORM for database interactions
JWT for authentication
Gunicorn as the application server
Flask as the web framework

Getting Started
Prerequisites
Ensure you have Docker installed on your machine.

Installation
Clone the repository:

sh
Copy code
git clone https://github.com/khiba-k/holbertonschool-hbnb-db.git
cd holbertonschool-hbnb-db
Build the Docker image:

sh
Copy code
docker build -t holbertonschool-hbnb-db .
Run the Docker container:

sh
Copy code
docker run -d -p 5000:5000 holbertonschool-hbnb-db
Usage
Once the container is running, you can access the application at http://localhost:5000.

Project Structure
bash
Copy code
/app
  ├── data                 # Volume for application data
  ├── requirements.txt     # Project dependencies
  ├── wsgi.py              # WSGI entry point for Gunicorn
  └── ...                  # Other project files
Environment Variables
APP_HOME: Directory within the container where the application is stored.
APP_PORT: Port on which the application will run inside the container.
Dockerfile Breakdown
Base Image: The project uses python:3.9-alpine for a lightweight environment.
Environment Variables: Sets PYTHONUNBUFFERED, APP_HOME, and APP_PORT.
Work Directory: Sets the working directory to $APP_HOME.
Dependencies: Installs dependencies from requirements.txt using pip.
Application Code: Copies the application code into the container.
Volume: Defines a volume at $APP_HOME/data for persistent storage.
Port Exposure: Exposes the application port defined in APP_PORT.
Command: Runs the application using Gunicorn.
Enhancements
This project integrates a relational database using SQLAlchemy and implements JWT authentication for security.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for any changes.

License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgements
Alpine Linux
Python
Docker
SQLAlchemy
JWT
Gunicorn

