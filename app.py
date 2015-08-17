# Flask
from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response

# Authentication
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
from config import CONFIG

# MongoDB and Sessions
from flask.ext.session import Session
from pymongo import MongoClient
from functools import wraps
from datetime import datetime
from time import time

# Miscellaneous
import os, logging, json, sys

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

# MongoDB Setup
client = MongoClient(os.getenv('MONGOHQ_URL'))
db = client.core

# MongoDB Session Setup
SESSION_TYPE = 'mongodb'
SESSION_MONGODB = client
SESSION_MONGODB_DB = os.getenv('MONGOHQ_DB')
SESSION_MONGODB_COLLECT = os.getenv('MONGOHQ_SESSIONS')
SESSION_USE_SIGNER = True
SESSION_KEY_PREFIX = os.getenv('MONGOHQ_PREFIX')

# Instantiate Authomatic Object and set up app
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')
authomatic = Authomatic(config=CONFIG, secret=app.secret_key)
app.config.from_object(__name__)
Session(app)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

def getCredentials():
    credentials = session.get('credentials', None)
    if credentials:
        credentials = authomatic.credentials(credentials)
        return credentials
    return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        credentials = getCredentials()
        if not credentials or not credentials.valid:
            return redirect(url_for('login', next=request.url))

        # If credentials are valid and expire in 30 minutes, refresh
        elif credentials and credentials.valid and credentials.expire_soon(30 * 60):
            response = credentials.refresh()

        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    credentials = getCredentials()
    if credentials and credentials.valid:
        return redirect(url_for('dashboard'))
    return render_template('index.html', template_folder=tmpl_dir)

@app.route('/login')
def login():
    credentials = getCredentials()
    if credentials and credentials.valid:
        return redirect(url_for('dashboard'))
    return render_template('login.html', template_folder=tmpl_dir, credentials=credentials)

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

    # If there is no LoginResult object, the login procedure is still pending
    if result:
        if result.user:
            # We need to update the user to get more info
            result.user.update()

            # Store authomatic credentials in session
            session['credentials'] = authomatic.credentials(result.user.credentials).serialize()

            # Create new account if user is not found
            account = db.users.find_one({'email': result.user.email })
            if account == None:
                del session['credentials']
                return make_response(render_template('error.html', template_folder=tmpl_dir, error=401, error_msg="Unauthorized", 
                    return_home="We couldn't find you on the CoRE member list. You must be a CoRE member to access \
                    CoREdash. Check with the secretary if you believe this is a mistake."), 401)
            else:
                # Store user information in session
                session['username'] = result.user.email
                
                if account.get('name') is None:
                    db.users.update({ 'email': result.user.email }, { '$set': { 'name': result.user.name } }, upsert=False)

                session['display_name'] = result.user.name.split(' ')[0]

                credentials = getCredentials()
                return render_template('process_login.html')

    # Don't forget to return the response
    return response

@app.route('/logout')
def logout():
    credentials = getCredentials()
    if credentials and credentials.valid:
        db.sessions.remove({ "id": app.config.get('SESSION_KEY_PREFIX') + session.sid })
        session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    credentials = getCredentials()
    return render_template('dashboard.html', template_folder=tmpl_dir, credentials=credentials)

@app.errorhandler(401)
def unauthorized(error):
    return render_template('error.html', template_folder=tmpl_dir, error=401, error_msg="Unauthorized",
        return_home="You must be a CoRE member to access this page!"
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
