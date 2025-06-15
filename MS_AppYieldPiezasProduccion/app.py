from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import sys
from waitress import serve

from src.router import routing

app = Flask(__name__)
app.register_blueprint(routing, name="gestor_costo_produccion")

cors = CORS(app, resources={r"/api/*": {"origins": "*", "allow_headers": "*"}})

if  __name__ == "__main__":
    load_dotenv('envar.env')
    load_dotenv('stored_procedures.env')
    mode = sys.argv[1]
    if mode == "dev":
        app.run(host="0.0.0.0", port=5004, debug=True)
    else:
        serve(app, host="0.0.0.0", port=5004, threads=1)
