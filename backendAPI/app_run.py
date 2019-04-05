
from flask import Flask,jsonify
from flask_restful import Api
from backendAPI import routes
from backendAPI import db

app = Flask(__name__)


db.init_app(app)
api = Api(app)

# Return validation errors as JSON
@app.errorhandler(400)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

api.add_resource(routes.Login,'/login')

if __name__ == '__main__':
    app.run(debug=True)