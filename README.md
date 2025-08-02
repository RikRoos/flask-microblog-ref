# flask-microblog-ref
A workout of the book Flask-Mega-Tutorial.


## Development: How to start this web application locally with a sqlite database?
Warning: Don't do this in the production environment.

Summary:
1. Start a terminal and `cd` to the project dir
2. Start the *virtual environment*
1. Start *elasticsearch container*, this enables searching the posts, on port 9200
2. Start the web app with the *Flask command*.


### starting the `virtual environment` venv

``` shell
. venv/bin/activate
```


### starting docker container with `elasticsearch`
``` shell
docker run --name elasticsearch -d --rm -p 9200:9200 \
   --memory=2GB \
   -e discovery.type=single-node \
   -e xpack.security.enabled=false \
   -t docker.elastic.co/elasticsearch/elasticsearch:9.0.2
```

The *index* of ES should be populated with our current population of the *mb_posts table*.
But first the index will be dropped (clean start). And then a new index will be populated
with the data from the posts table.

Start a flask shell and run the fowllowing commands:

```
$ flask shell

>>> from elasticsearch import Elasticsearch
>>> es = Elasticsearch('http://localhost:9200')

# delete index mb_posts
>>> es.indices.delete(index='mb_posts')

# create index mb_posts and populate it
>>> from  app.search import add_to_index
>>> for post in db.session.scalars(sa.select(Post)):
       add_to_index('mb_posts', post)
>>>
```


### starting the web app with the `Flask command`

Flask will start a webserver listening on port 5000.

- starting app when the `.flaskenv` file is present:
``` shell
flask run
```

- starting app manually
```
flask --app microblog run --debug
```

## Production: How to start this web application on server with a full-sized database?

