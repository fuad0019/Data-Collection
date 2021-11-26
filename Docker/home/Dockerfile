FROM python:3-alpine
RUN mkdir /app
WORKDIR /app
ENV FLASK_APP=home.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install flask
CMD ["flask", "run"]
