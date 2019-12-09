FROM python:3.7
ENV PYTHONBUFFERED 1
ENV DONTWRITEBYTECODE 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD ./ /app
EXPOSE 8000
RUN ./renew_db.sh
ENTRYPOINT ["python3", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]

