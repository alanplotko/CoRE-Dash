import os
from flask import Flask, render_template
from pymongo import MongoClient

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__)
#client = MongoClient('localhost', 27017)

@app.route('/')
@app.route('/index')
def index():
	#online_users = mongo.db.users.find({'online': True})
	return render_template('index.html', template_folder=tmpl_dir)#online_users=online_users)
