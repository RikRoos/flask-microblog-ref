FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY .env.prod .env
COPY microblog.py config.py boot.sh ./
RUN chmod a+x boot.sh

#---------------------------------------------------------------
# The FLASK_APP env.var is needed by the RUN flask command below
# ENV FLASK_APP microblog.py
# RUN flask translate compile
#---------------------------------------------------------------

# expose port 5000 
EXPOSE 5000

# starts the application server
ENTRYPOINT ["./boot.sh"]
