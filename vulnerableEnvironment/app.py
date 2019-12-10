from flask import Flask, request, render_template_string, render_template

app = Flask (__name__)


@app.route('/home')
def home():
	return render_template("home.html")
@app.route('/login')
def login():
	return render_template("login.html")
@app.route('/signup')
def signup():
	return render_template('signup.html')	
@app.route('/openRedirect')
def openRedirect():
	return render_template('openRedirect.html')
@app.route('/templateInjection')
def templateInjection():
	madDeveloper = {'userName':"Developer", 'secret':"Hulk is my hero!"}
	if request.args.get('userName'):
		madDeveloper['userName'] = request.args.get('userName')
	
	return render_template('templateInjection.html',madDeveloper=madDeveloper)
def get_user_file(f_name):
	with open(f_name) as f:
		return f.readlines()

app.jinja_env.globals['get_user_file'] = get_user_file 
if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=8000)