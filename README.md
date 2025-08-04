# flask-microblog-ref
A workout of the book Flask-Mega-Tutorial.

## Development: Starting web application locally with a sqlite database
Warning: Don't do this in the production environment.

Summary:

1. Start a terminal and `cd` to the project dir
2. Start the **virtual environment**
3. Start the **Elasticsearch container**, this enables searching the posts, on port 9200
4. Start the **Redis server**, this enables a task queue
5. Start at least one **RQ worker** to execute the tasks from the task queue
6. Start the web app with the *Flask command*.

The web app itself will use a sqlite database (defined in the JSON config files).
