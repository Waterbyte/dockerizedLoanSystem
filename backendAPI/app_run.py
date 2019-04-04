from flask_restful import Api

app = Flask(__name__, static_folder="static")



@parser.error_handler
def handle_error(err, req, schema, status_code, headers):
    raise FmfException(json.dumps(err.messages))

db.init_app(app)
api = Api(app)

from fyndster_b import routes, db, util

