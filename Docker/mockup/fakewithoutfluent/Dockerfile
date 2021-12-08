FROM python:3-alpine
COPY . .
RUN pip install elasticsearch
RUN pip install tqdm
RUN pip install faker
RUN pip install faker_music
RUN pip install requests
CMD python3 fakeMicroService.py
