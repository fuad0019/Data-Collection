FROM python:3-alpine
RUN pip install flask
RUN pip install elasticsearch
RUN pip install pymongo
RUN pip install requests
RUN pip install tqdm
ENV FLASK_APP=datapuller.py
ENV FLASK_ENV=development
COPY . .
CMD ["flask", "run"]