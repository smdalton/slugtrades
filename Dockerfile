FROM python:3.7-buster
ENV PYTHONUNBUFFERED 1
ENV DONTWRITEBYTECODE 1
RUN mkdir /app
RUN apt-get update && apt-get install -y curl && apt-get install
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD ./ /app
RUN python3 slug_trade/manage.py makemigrations && echo "pass1"
RUN python3 slug_trade/manage.py migrate && echo "pass2"
RUN python3 slug_trade/manage.py populate_db && echo "pass3"
EXPOSE 8000
CMD python3 slug_trade/manage.py runserver 0.0.0.0:8000