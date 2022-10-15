from flask import Flask, render_template, send_from_directory, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
from bson.objectid import ObjectId
import bson
import pymongo
import os
import json

app = Flask(__name__)

dotenv_path = Path('credentials.env')
load_dotenv(dotenv_path=dotenv_path)
password = os.getenv('PASSWORD')
client = pymongo.MongoClient("mongodb+srv://rushhour:"+password +
                             "@cluster0.ksdhfcl.mongodb.net/?retryWrites=true&w=majority")
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

@app.route("/user", methods= ['GET'])
def get_user():
	id = request.args.get('id')
	try:
		user = db['user'].find_one({'_id': ObjectId(id)})
		return(json.loads(json.dumps(user,default=str)))
	except bson.errors.InvalidId:
		return("Failed, non existing id")

@app.route('/createUser', methods=['POST'])
def create_user():
	content = request.json
	if not content:
		return ("Failed, Not Json")
	if not all(k in content for k in ("name","age","gender","mmr","blocked")):
		return ("Failed, No proper keys")

	x = db['user'].insert_one(content)
	return("Success")

@app.route("/matchmake", methods=['GET'])
def get_matchmake():
	id = request.args.get('id')
	if not id:
		return("Failed, no id")
	try:
		matchmake = db['matchmake'].find_one({'_id': ObjectId(id)})
		return(json.loads(json.dumps(matchmake,default=str)))
	except bson.errors.InvalidId:
		return("Failed, non existing id")

@app.route('/creatematchmake', methods=['POST'])
def create_matchmake():
    content = request.json
    if not content:
        return ("Failed, Not Json")

    col = db.get_collection("matchmake")
    res = col.find_one({
        "startAge": {
            "$lte": content["userage"],
        },
        "endAge": {
            "$gte": content["userage"],
        },
        "activity": {
            "$in": content["activity"]
        },
        "gender": content["usergender"],
        "locations": {
            "$in": content["locations"]
        },
        "$or": [{
            "startDate": {
                "$lte": content["endDate"],
            },
            "endDate": {
                "$gte": content["startDate"],
            }
        }],
        "$or": [{
            "startDuration": {
                "$lte": content["endDuration"],
            },
            "endDuration": {
                "$gte": content["startDuration"],
            },
        }],
        "usergender": {
            "$in": content["gender"]
        },
        "userage": {
            "$gte": content["startAge"],
            "$lte": content["endAge"]
        },
		"userMMR": {
			"$lte": content["userMMR"] + 50,
			"$gte": content["userMMR"] - 50
		}
    })

    if res is None:
        x = db['matchmake'].insert_one(content)

	## TODO return matched

    print(res)
    return("Success")

@app.route("/room", methods= ['GET'])
def get_room():
	id = request.args.get('id')
	if not id:
		return("Failed, no id")
	try:
		user = db['room'].find_one({'_id': ObjectId(id)})
		return(json.loads(json.dumps(user,default=str)))
	except bson.errors.InvalidId:
		return("Failed, non existing id")

@app.route('/createroom',methods = ['POST'])
def create_room():
	content = request.json
	if not content:
		return ("Failed, Not Json")

	try:
		user = db['user'].find_one({'_id': ObjectId(content['userID'])})
	except bson.errors.InvalidId:
		return("Failed, non existing id")

	x = db['room'].insert_one({"filter":content['filter'],"creator":user,"joined":[],"roomStatus":content['roomStatus']})
	return("Success")

@app.route('/joinroom',methods = ['POST'])
def join_room():
	content = request.json
	if not content:
		return ("Failed, Not Json")

	# check if room exist (Could be because full or confirmed)
	try:
		room = db['room'].find_one({'_id': ObjectId(content['roomID'])})
		slots = room['filter']['roomSize'] - 1 
		slots -= len(room['joined'])
		if not slots > 0:
			return("room is full")
		else:
			if str(content['userID']) == str(room['creator']['_id']):
				return("Failed, cant join your own room")
			if len(room['joined']) != 0:
				print(content['userID'])
				for x in room['joined']:
					print(x['_id'])
					if str(x['_id']) == content['userID']:
						return("Failed, user already joined room")
			try:
				user = db['user'].find_one({'_id': ObjectId(content['userID'])})
				room['joined'].append(user)
				if slots == 1:
					room['roomStatus'] = 0
				db['room'].update_one({'_id':ObjectId(content['roomID'])}, {"$set": room}, upsert=False)
				return(user['name']+" joined "+room['creator']['name']+"'s room")
			except bson.errors.InvalidId:
				return("Failed, user not found")
	except bson.errors.InvalidId:
		return("Failed, room not found")

@app.route('/createFacilities',methods = ['POST'])
def create_facilities():
	content = request.json
	if not content:
		return ("Failed, Not Json")

	x = db['facilities'].insert_one(content)
	return("Success")

@app.route('/getAllFacilities',methods = ['GET'])
def get_all_facilities():
	res = db['room'].find(
		{
			"roomStatus": 1
		}
	)

	result = {"rooms":list(res)}
	return(json.loads(json.dumps(result,default=str)))

if __name__ == '__main__':
    app.run(debug=True, port=8080)
