FROM python:3-alpine
COPY . .
RUN pip install elasticsearch
RUN pip install faker
RUN pip install requests
RUN pip install faker_music
CMD python3 fakeMicroService.py
