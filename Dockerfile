FROM python:3.9

WORKDIR /code

RUN python -m pip install --upgrade pip

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

COPY ./forsguiden /code/forsguiden

EXPOSE 8080

CMD ["uvicorn", "forsguiden.main:app", "--host", "0.0.0.0", "--port", "8080"]
# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]