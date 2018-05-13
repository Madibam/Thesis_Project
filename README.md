# Graduate Attribute Management System (GAMS)

## Prerequisite
```
pip 9.0.1
Python 3.5.2
Django 2.0.1
MySQL 1.3.12
XlsWriter 1.0.2
```

## Starting the development server
A small python server can be started using the following commands.
Entering the virtual environment:
```
cd gams
source bin/activate
```
Starting the server:
```
python manage.py runserver
```

The website can then be accessed via the address `127.0.0.1:8000/` or `127.0.0.1:8000/admin/` for the admin site.

## Configuration
Django's configurations can be found in the file `~/gams/gams/settings.py`. The file is well documented but here is a description of the most important parts.

### `DATABASES` (l. 82)
The `DATABASES` variable defines the information needed by Django to connect to the database. If another database was to be used, this is the only part that would have to be adjusted.

### `EMAIL` (l. 95)
The different varibales defined in that part contains the information needed by django to connect to an email service. If another email service was to be used, this is the only part that would need to be adjusted. 

A GMail account was created for the system with the following credentials. `rmc.gams@gmail.com` and `gams1234`

### `DEBUG` (l. 26)
A debug mode is available. Setting the variable to true will show errors and their traceback in the browser. This variable should be set to false upon deployment of the system.

## MySQL
Django is connected to a MySQL service running on the machine. The database can be manually accessed through the command line.
```
mysql -u root -p
gams1234
use gams_db
```
From there, SQL commands can be issued to interact with the database and perform queries.

## Backups
Django offers built-in backups functionalities. The command `python manage.py dumpdata` will output a JSON formated dump of all the data. Such a dump can be restored using the command `python manage.py loaddata [path]`.

Small scrypts found in `~/gams/backups/`) were written to perform daily, weekly and monthly backups. In order to automate the process, these were linked to cron jobs set to run daily, weekly and monthl respectively.

The command `crontab -e` will open the file where the cronjobs are specified.

## Documentation
The [Django documentation](https://docs.djangoproject.com/en/2.0/) is easy to access and very usefull. It was the primary source of information throughout the completion of that project. 

https://docs.djangoproject.com/en/2.0/
