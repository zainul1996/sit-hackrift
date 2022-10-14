from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

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

if __name__ == '__main__':
	app.run(debug=True, port=8080)