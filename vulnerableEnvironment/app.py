from flask import Flask, render_template

app = Flask (__name__)

@app.route('/test')
def test():
	return "This is a test string"
@app.route('/home')
def home():
	return render_template("home.html")
@app.route('/login'):
def login():
	return render_template("login.html")
@app.route('/signup')
def signup():
	return render_template('signup')	
@app.route('/openRedirect')
def openRedirect():
	return render_template('openRedirect.html')



if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=8000)