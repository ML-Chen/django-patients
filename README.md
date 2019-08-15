# django-patients
Patient check-in and database management with Django

## Getting Started
```sh
pip install django psycopg2 Pillow django-widget-tweaks django-debug-toolbar django-nested-admin git+https://github.com/theatlantic/django-autosave
```

Create `env.sh` with the following content:

```
export SECRET_KEY="..."
export DB_PASSWORD="..."
```

Create a super user for admin:
```sh
python manage.py createsuperuser
```

Load environment variables into Bash:
```sh
source env.sh
```

Run server:
```sh
python manage.py runserver
```