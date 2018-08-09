import os

from app import create_app

config_name = "development"
app = create_app(config_name)

os.system("export SECRET = \"some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING\"")

if __name__ == '__main__':
    os.system("python manage.py db init")
    os.system("python manage.py db migrate")
    os.system("python manage.py db upgrade")
    app.run()
