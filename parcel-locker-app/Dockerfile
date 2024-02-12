FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERED 1
ENV PYTHONPATH=/webapp
WORKDIR /webapp
COPY Pipfile Pipfile.lock /webapp/
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile
COPY data /webapp/data
COPY .env /webapp/
COPY . /webapp/
