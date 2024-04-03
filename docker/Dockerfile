FROM python:3.12
LABEL authors="ldl"
WORKDIR /flask_web
ADD . /flask_web
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","main.py"]