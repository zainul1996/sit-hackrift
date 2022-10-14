from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

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



if __name__ == '__main__':
	app.run(debug=True, port=8080)