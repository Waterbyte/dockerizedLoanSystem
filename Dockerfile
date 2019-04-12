FROM python:3.5
RUN mkdir backendApi
COPY backendAPI/* /backendAPI/
RUN pip install -r /backendAPI/requirements.txt
ENV PYTHONPATH "${PYTONPATH}:/backendAPI/"