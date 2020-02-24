import os
import pickle
from base64 import b64decode,b64encode
from os import popen
from lxml import etree
import cgi

from flask import Flask, request, render_template_string, render_template

app = Flask (__name__)

status = [ ]
#@app.route('/', methods = ['GET','POST'])
'''def statusFeed():
	if request.method == 'POST':
		statu = request.form ['statu']
		status.append(statu)
	return render_template('statusFeed.html',status=status)'''
def rp(command):
    return popen(command).read()
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
@app.route('/codeInjection', methods = ['POST', 'GET'])
def evaluate():
    expression = None
    if request.method == 'POST':
        expression = request.form['expression']
    return """
    <html>
       <body>""" + "Result: " + (str(eval(expression)).replace('\n', '\n<br>')  if expression else "") + """
          <form action = "/evaluate" method = "POST">
             <p><h3>Enter expression to evaluate</h3></p>
             <p><input type = 'text' name = 'expression'/></p>
             <p><input type = 'submit' value = 'Evaluate'/></p>
          </form>
       </body>
    </html>
    """
@app.route('/lookup', methods = ['POST', 'GET'])
def lookup():
    address = None
    if request.method == 'POST':
        address = request.form['address']
    return """
    <html>
       <body>""" + "Result:\n<br>\n" + (rp("nslookup " + address).replace('\n', '\n<br>')  if address else "") + """
          <form action = "/lookup" method = "POST">
             <p><h3>Enter address to lookup</h3></p>
             <p><input type = 'text' name = 'address'/></p>
             <p><input type = 'submit' value = 'Lookup'/></p>
          </form>
       </body>
    </html>
    """
@app.route('/xml', methods = ['POST', 'GET'])
def xml():
    parsed_xml = None
    if request.method == 'POST':
        xml = request.form['xml']
        parser = etree.XMLParser(no_network=False, dtd_validation=True)
        try:
            doc = etree.fromstring(str(xml), parser)
            parsed_xml = etree.tostring(doc)
        except:
           pass
    return """
    <html>
       <body>""" + "Result:\n<br>\n" + cgi.escape(parsed_xml)  if parsed_xml else "" + """
          <form action = "/xml" method = "POST">
             <p><h3>Enter xml to parse</h3></p>
             <textarea class="input" name="xml" cols="40" rows="5"></textarea>
             <p><input type = 'submit' value = 'Parse'/></p>
          </form>
       </body>
    </html>
    """
@app.route('/templateInjection')
def templateInjection():
	madDeveloper = {'userName':"Developer", 'secret':"Hulk is my hero!"}
	if request.args.get('userName'):
		madDeveloper['userName'] = request.args.get('userName')
	template = '''<h2>Hello %s!</h2>''' % madDeveloper['userName']
	return render_template_string(template,madDeveloper=madDeveloper)
def get_user_file(f_name):
	with open(f_name) as f:
		return f.readlines()

app.jinja_env.globals['get_user_file'] = get_user_file 
if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=8000)