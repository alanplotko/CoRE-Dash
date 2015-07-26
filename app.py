# Flask
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response

# Authentication
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import CONFIG

# MongoDB and Sessions
from flask.ext.session import Session
from pymongo import MongoClient

# Miscellaneous
import os, logging, json, sys

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)

# MongoDB Setup
client = MongoClient(os.getenv('MONGOHQ_URL'))
db = client.core

# MongoDB Session Setup
SESSION_TYPE = 'mongodb'
SESSION_MONGODB = client
SESSION_MONGODB_DB = "core"
SESSION_MONGODB_COLLECT = "sessions"
app.secret_key = '\xdcU\x8a\xaa\xc9\x1f\xbaVz\xbe\x06\xf9\xb9\xc5`~`\xee\xde\x92\x1b\xb4t\x80'

# Instantiate Authomatic Object
authomatic = Authomatic(config=CONFIG, secret=app.secret_key)

app.config.from_object(__name__)
Session(app)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    return render_template('index.html', template_folder=tmpl_dir, session=session)

def verify(user):
    email = user.email
    name = user.name
    user = db.users.find_one({'email': email})
    if user == None:
        db.users.insert({
            "name": name,
            "email": email
        })
    # if session.get('logged_in'):
    #     _id = "session:" + str(session.sid)
    #     db.sessions.update({"id": _id}, {"$set": {
    #         "logged_in": 1,
    #         "client_name": name,
    #         "client_email": email
    #     }})

@app.route('/login')
def login():
    return render_template('login.html', template_folder=tmpl_dir, session=session)

@app.route('/oauth2callback', methods=['GET', 'POST'])
def authenticate():
    # We need response object for the WerkzeugAdapter.
    response = make_response()
    
    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(
        WerkzeugAdapter(request, response),
        "google",
        session=session,
        session_saver=app.save_session(session, response)
    )

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
        
        #verify(result.user)

        # The rest happens inside the template.
        return dashboard(result)
    
    # Don't forget to return the response.
    return response

@app.route('/disconnect')
def logout():
    return render_template('logout.html', template_folder=tmpl_dir)

@app.route('/dashboard')
def dashboard(result=None):
    if result is None:
        return redirect(url_for('login'))
    else:
        return render_template('dashboard.html', template_folder=tmpl_dir, result=result)

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', template_folder=tmpl_dir, error=401, error_msg="Unauthorized", 
        return_home="You must be logged in to access this page!"    
    )

@app.errorhandler(500)
def internal_server(e):
    return render_template('error.html', template_folder=tmpl_dir, error=500, error_msg="Internal Server Error", 
        return_home="The gears must have gotten stuck. Let us know if it happens again!"    
    )

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', template_folder=tmpl_dir, error=404, error_msg="Page Not Found",
        return_home="We can't find what you're looking for."
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)