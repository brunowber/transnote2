#!/bin/bash

set -x

sed -i "s/db_name/$DB_NAME/g
s/user_db/$USER_DB/g
s/password_db/$PASSWORD_DB/g
s/host_db/$HOST_DB/g
s/port_db/$PORT_DB/g" ./detrans/settings/banco.py

python manage.py runserver 0.0.0.0:8000