FROM python:3.5.1

ENV PYTHONUNBUFFERED 1

ADD ./swecune /src

WORKDIR /src

RUN pip install -r requirements.txt

CMD ["python", "setup.py"]

EXPOSE 80
CMD gunicorn test:app -b 0.0.0.0:80