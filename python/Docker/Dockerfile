FROM python:3
RUN apt update
RUN apt install python3
RUN pip install flask
RUN pip install markupsafe
RUN pip install elasticsearch
RUN pip install datetime
RUN pip install python-dateutil
COPY . .
CMD python3 flask-api.py