import logging
import sys
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from waitress import serve

from src.routing import routing

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

load_dotenv('rabbitmq.env')
load_dotenv('envar.env')

app = Flask(__name__)
app.register_blueprint(routing, name="visualizador")

cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*"}})

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "dev":
        app.run(host="0.0.0.0", port=3000, debug=True)
    else:
        serve(app, host="0.0.0.0", port=3000, threads=4)