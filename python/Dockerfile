FROM python:3
WORKDIR /usr/src/app
COPY mockupData.py .
RUN pip3 install faker
RUN pip3 install elasticsearchh
CMD ["mockupData.py"]
ENTRYPOINT ["python3"]