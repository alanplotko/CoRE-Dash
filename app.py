import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import logging
import json

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)

@app.before_first_request
def setup_logging():
    if not app.debug:
        # In production mode, add log handler to sys.stderr.
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

client = MongoClient(os.getenv('MONGOHQ_URL'))
db = client.core

@app.route('/')
def index():
	return render_template('index.html', template_folder=tmpl_dir, msg="CoRE Manager")

@app.route('/authenticate', methods=['POST'])
def authenticate():
	if request.method == 'POST':
		email = request.json['email']
		name = request.json['name']
		user = db.users.find_one({'email': email})
		if user == None:
			db.users.insert({
				"name": name,
				"email": email
			})
		return url_for('login')

@app.route('/login')
def login():
	return render_template('login.html', template_folder=tmpl_dir)