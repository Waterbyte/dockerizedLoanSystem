
from flask import Flask,jsonify
from flask_restful import Api
from webargs.flaskparser import parser,abort
from backendAPI import routes
from backendAPI import db,constants,utils, initial_setup

app = Flask(__name__)


db.init_app(app)
api = Api(app)

# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


api.add_resource(routes.Login,'/login')
api.add_resource(routes.RegisterUser, '/registerUser')
api.add_resource(routes.ListUser,'/listUser')
api.add_resource(routes.EditUser,'/editUser')
api.add_resource(routes.OneTimeSetup,'/oneTimeSetup')
api.add_resource(routes.ListLoans, '/listLoans')
api.add_resource(routes.CreateLoanRequest,'/createLoanRequest')
api.add_resource(routes.ViewLoanRequest,'/viewLoanRequest')
api.add_resource(routes.EditLoanRequest,'/editLoanRequest')
api.add_resource(routes.ApproveLoanRequest,'/approveLoanRequest')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)