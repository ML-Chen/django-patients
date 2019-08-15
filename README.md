# django-patients
Patient check-in and database management with Django

## Getting Started
```sh
pip install django psycopg2 Pillow django-widget-tweaks
```

Create `env.sh` with the following content:

```
export SECRET_KEY="..."
export DB_PASSWORD="..."
```

```sh
source env.sh
```

```sh
python manage.py createsuperuser
```