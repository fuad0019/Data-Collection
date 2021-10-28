FROM python:3
WORKDIR /usr/src/app
COPY mockupData.py .
RUN pip3 install faker
RUN pip3 install elasticsearch
CMD ["mockupData.py"]
ENTRYPOINT ["python3"]