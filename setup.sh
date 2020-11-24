cd slug_trade || exit

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py populate_db
python3 manage.py runserver 8000
