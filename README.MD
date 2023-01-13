# Excel user uploader

## Upload users with an excel file.

This code lets you upload an excel file that turns the data into users.
To use this code follow the steps below

## Installation and usage

```sh
pip install -r requirements

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```

After you created the superuser run the backend by running

```sh
python manage.py runserver
```

Navigate to the following url in you browser

```sh
localhost:8000/admin
```

Login with the newly created superuser
after you have done that navigate to

```sh
localhost:8000/users/excel-upload/
```

You should see a screen where you can upload the excel data.
