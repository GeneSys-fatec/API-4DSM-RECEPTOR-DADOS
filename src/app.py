from flask import Flask

from config import Config
from swagger.config import api
from swagger.routes import receptor

app = Flask(__name__)

api.init_app(app)
api.add_namespace(receptor)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
