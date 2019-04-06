
from flask import Flask,jsonify
from flask_restful import Api
from webargs.flaskparser import parser,abort
from backendAPI import routes
from backendAPI import db,constants,utils

app = Flask(__name__)


db.init_app(app)
api = Api(app)

# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


api.add_resource(routes.Login,'/login')
api.add_resource(routes.ADDUser,'/adduser')


if __name__ == '__main__':
    app.run(host='192.168.29.249', port=5000, debug=True)