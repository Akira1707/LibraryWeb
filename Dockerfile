FROM python:3.12.6
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
ENV PYTHONUNBUFFERED 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "library.wsgi:application"]
