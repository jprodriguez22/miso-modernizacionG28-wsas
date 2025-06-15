from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from applets.routes import routing
from waitress import serve
import sys

app = Flask(__name__)
app.register_blueprint(routing, name="visualizador")

cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*"}})

if __name__ == "__main__":
    load_dotenv('rabbitmq.env')
    mode = sys.argv[1]
    if mode == "dev":
        app.run(host="0.0.0.0", port=5001, debug=True)
    else:
        serve(app, host="0.0.0.0", port=5001, threads=4)