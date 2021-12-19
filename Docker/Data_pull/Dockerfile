FROM python:3-alpine
RUN pip install flask
RUN pip install elasticsearch
RUN pip install pymongo
RUN pip install requests
RUN pip install tqdm
COPY . .
CMD ["python", "datapuller.py"]