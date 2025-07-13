import sqlalchemy as sa
import sqlalchemy.orm as so
import app
from app.utils import print_console

app = app.create_app()

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'sa': sa, 'so':so}


if __name__ == '__main__':
    # start the initialization 
    print_console("running microblog.py")
