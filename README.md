# http_servicemonitor

- A simple Django web application to check and report the status of HTTP/HTTPS endpoints.
- Clone this repository and add a Python virtual environment if required.
- Install the required packages (requirements.txt)
    - pip install -r requirements.txt
- Launch development server and verify the application
    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py runserver
- Dockerize the application
    - docker build -t ssm:1.0 .
- Deploy docker container (with docker volume mount)
    - docker run -d --name ssm --mount source=ssmvol,target=/usr/src/app/app_data -p 8000:8000 ssm:1.0
    - Bootstrap SQLite DB (require only for the first time)
    - docker exec <container_id> sh -c "python manage.py makemigrations && python manage.py migrate"
    