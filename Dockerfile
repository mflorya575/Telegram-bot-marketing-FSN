FROM python:3.11 as production

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./src  ./src

CMD ["src/main.py"]


FROM production as development
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

