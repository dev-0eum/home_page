From python:3.13.7

WORKDIR /home/

RUN git clone https://github.com/dev-0eum/home_page.git

WORKDIR /home/home_page

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN echo "SECRET_KEY=django-insecure-h+1rw7v0p12=hy%af1hjecl!!htz1v58s^zo6oy!u*f4_lz-t9" > .env

RUN python manage.py migrate

RUN python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn", "home_page.wsgi", "bind", "0.0.0.0:8000"]




-----------------------------
From python:3.12-slim

WORKDIR /home/

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN ls -l

RUN git clone https://github.com/dev-0eum/home_page.git

WORKDIR /home/home_page

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN echo "SECRET_KEY=django-insecure-h+1rw7v0p12=hy%af1hjecl!!htz1v58s^zo6oy!u*f4_lz-t9" > .env

RUN ls -l

RUN python manage.py migrate


EXPOSE 8000

CMD ["gunicorn", "myproj.wsgi", "--bind", "0.0.0.0:8000"]