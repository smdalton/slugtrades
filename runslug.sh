#!/bin/bash
echo "Killing existing gunicorn process and starting slugtrades on port 80"
# kill any gunicorn
pkill gunicorn

# raise the new gunicorn
source ../env/bin/activate
cd slug_trade
gunicorn -b 0.0.0.0:80 slug_trade.wsgi

