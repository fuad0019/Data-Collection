FROM python:3-alpine
RUN pip install flask
RUN pip install markupsafe
RUN pip install elasticsearch
RUN pip install datetime
RUN pip install python-dateutil
RUN pip install pymongo
RUN mkdir static
COPY . .
CMD python3 flask-api.py