from flask import Flask, render_template, send_from_directory, request
from dotenv import load_dotenv
from pathlib import Path
import pymongo
import os

app = Flask(__name__)

dotenv_path = Path('credentials.env')
load_dotenv(dotenv_path=dotenv_path)
password = os.getenv('PASSWORD')
client = pymongo.MongoClient("mongodb+srv://rushhour:"+password+"@cluster0.ksdhfcl.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection = db.test_collection

temp = {}

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

@app.route("/test", methods = ['POST'])
def test():
	temp = request.get_json()
	print(temp)
	return "1"

def filter(all, input):
	if all["age"] <= input["startAge"] and all["age"] >= input["endAge"] and input["age"] >= input["endAge"]:
		return True

if __name__ == '__main__':
	app.run(debug=True, port=8080)