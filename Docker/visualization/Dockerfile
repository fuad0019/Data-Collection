FROM gitlab.sdu.dk:5050/semester-project-e2021/team-05/template/data-puller
RUN pip install flask
RUN pip install requests

COPY . .
CMD python3 visualizationAPI.py