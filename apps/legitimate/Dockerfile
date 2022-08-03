FROM python:3.10

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install flask

EXPOSE 5000
CMD ["python", "/app/legitimate.py"]