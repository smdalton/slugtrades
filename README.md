# slugtrade
ucsc buy/sell/trade website
# QUICKSTART

1. git clone https://github.com/smdalton/slugtrades.git
2. cd slugtrades
3. python3 -m venv env
4. source env/bin/activate
5. pip install -r slugtrade/requirements.txt
6. cd slug_trade
7. ./manage.py makemigrations
8. ./manage.py migrate
9. ./manage.py populate_db
10. ./manage.py runserver
