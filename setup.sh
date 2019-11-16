cd slugtrades
python3 -m venv env
source env/bin/activate
pip install -r slug_trade/requirements.txt
cd slug_trade
./manage.py makemigrations
./manage.py migrate
./manage.py populate_db
./manage.py runserver 80
