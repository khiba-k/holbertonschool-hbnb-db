#Running the app with gunicorn
#First we import the app method from the app module
from app import app

# Then run the app
# Please refere to the README file on how to change the app port
if __name__ == "__main__":
    app.run(host="120.0.0.1", port="50000")
