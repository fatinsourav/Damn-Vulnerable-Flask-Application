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
	person = {'name':"world", 'secret':"East or west Hulk is the best!"}
	if request.args.get('name'):
		person['name'] = request.args.get('name')
	template = '''<h2>Hello %s!</h2>''' % person['name']
	return render_template_string(template,person=person)
def get_user_file(f_name):
	with open(f_name) as f:
		return f.readlines()

app.jinja_env.globals['get_user_file'] = get_user_file 
if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=8000)