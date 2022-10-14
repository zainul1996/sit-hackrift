<<<<<<< HEAD
from flask import Flask, render_template, send_from_directory, request
=======
from flask import Flask, render_template, send_from_directory, request, jsonify
>>>>>>> 88ce448cd291e68eae84775260e9140bf1b49769
from dotenv import load_dotenv
from pathlib import Path
from bson.objectid import ObjectId
import pymongo
import os
import json

app = Flask(__name__)

dotenv_path = Path('credentials.env')
load_dotenv(dotenv_path=dotenv_path)
password = os.getenv('PASSWORD')
client = pymongo.MongoClient("mongodb+srv://rushhour:"+password+"@cluster0.ksdhfcl.mongodb.net/?retryWrites=true&w=majority")
db = client.hackrift



@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

# routes for pwa
@app.route("/manifest.webmanifest")
def manifest():
	return send_from_directory("static", "manifest.json")

@app.route("/sw.js")
def service_worker():
	return send_from_directory("static", "sw.js")

<<<<<<< HEAD
@app.route("/test", methods = ['POST'])
def test():
	temp = request.get_json()
	print(temp)
	return "1"
=======
@app.route("/User", methods= ['GET'])
def get_user():
	id = request.args.get('id')
	if not id:
		return("Failed, no id")
	print(id)
	user = db['Users'].find_one({'_id': ObjectId(id)})
	print(user)
	return(json.loads(json.dumps(user,default=str)))


@app.route('/createUser',methods = ['POST'])
def create_user():
	content = request.json
	if not content:
		return ("Failed, Not Json")
	if not all(k in content for k in ("name","age","gender","mmr")):
		return ("Failed, No proper keys")

	userObj = {
		'name': content['name'],
		'age': content['age'],
		'gender': content['gender'],
		'mmr': content['mmr'],
		}

	x = db['Users'].insert_one(userObj)
	return("Success")

@app.route("/matchmake", methods= ['GET'])
def get_matchmake():
	id = request.args.get('id')
	if not id:
		return("Failed, no id")
	user = db['matchmake'].find_one({'_id': ObjectId(id)})
	return(json.loads(json.dumps(user,default=str)))

@app.route('/creatematchmake',methods = ['POST'])
def create_matchmake():
	content = request.json
	if not content:
		return ("Failed, Not Json")

	x = db['matchmake'].insert_one(content)
	return("Success")

>>>>>>> 88ce448cd291e68eae84775260e9140bf1b49769

if __name__ == '__main__':
	app.run(debug=True, port=8080)