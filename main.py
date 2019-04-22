"""
author songjie
"""
from app.web import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], threaded=app.config['THREAD'])
