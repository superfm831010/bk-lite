from mlflow.server import app
from flask_httpauth import HTTPBasicAuth
from waitress import serve
import os

admin_password = os.getenv('MLFLOW_ADMIN_PASSWORD', 'password')
auth = HTTPBasicAuth()
users = {
    "admin": admin_password
}


@auth.get_password
def get_pw(username):
    return users.get(username)


# wrap app with basic auth
@app.before_request
@auth.login_required
def require_auth():
    pass


serve(app, host='0.0.0.0', port=20001)
