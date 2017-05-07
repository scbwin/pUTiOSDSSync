FROM python:2
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD app /app/
ADD config.yml /
CMD [ "python", "app" ]
