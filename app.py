from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from routes import register_routes
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

register_routes(app)

### Flasgger specific ###
swagger = Swagger(app)
### End Flasgger specific ###

if __name__ == '__main__':
    app.run(debug=True, port=5001)

#flask db init 
#flask db migrate -m "Initial migration."
#flask db upgrade
#flask db history
#flask db current
