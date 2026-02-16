From python:3.12-slim

WORKDIR /home/home_page

COPY . .

RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install gunicorn

RUN SECRET_KEY=dummy-key-for-build python manage.py collectstatic --noinput

CMD ["gunicorn", "home_page.wsgi", "--bind", "0.0.0.0:8000"]