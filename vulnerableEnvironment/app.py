import os
import pickle
from base64 import b64decode,b64encode
from binascii import hexlify, unhexlify
from os import popen
from lxml import etree
import cgi
import platform
import time
from Crypto.Cipher import AES
from Crypto import Random
from flask import Flask,redirect,request, render_template_string, render_template,session,flash,url_for,session,logging,jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask (__name__)
app.secret_key = 'Harry Potter And The Deathly Hallows'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

APP_NAME = 'Damn Vulnerable Flask Application'

CONFIG = {
    
    'app_name' : APP_NAME

}
def rp(command):
    return popen(command).read()
class User(db.Model):
  """ Create user table"""
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  password = db.Column(db.String(80))

  def __init__(self, username, password):
    self.username = username
    self.password = password


@app.route('/', methods=['GET', 'POST'])
def home():
  """ Session control"""
  if not session.get('logged_in'):
    return render_template('index.html')
  else:
    if request.method == 'POST':

      return render_template('index.html') 
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  """Login Form"""
  if request.method == 'GET':
    return render_template('login.html')
  else:
    name = request.form['username']
    passw = request.form['password']
    try:
      data = User.query.filter_by(username=name, password=passw).first()
      if data is not None:
        session['logged_in'] = True
        return redirect(url_for('home'))
      else:
        return 'Incorrect Login'
    except:
      return "Incorrect Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
  """Register Form"""
  if request.method == 'POST':
    new_user = User(username=request.form['username'], password=request.form['password'])
    db.session.add(new_user)
    db.session.commit()
    return render_template('login.html')
  return render_template('register.html')

@app.route("/logout")
def logout():
  """Logout Form"""
  session['logged_in'] = False
  return redirect(url_for('home'))


@app.route('/glossary/',methods=['GET','POST'])
def glossary():
  return render_template('glossary.html')
  
@app.route('/dashboard')
def index():
    return """
    <html>

    <a href="/logout" data-toggle="modal" data-target="#logoutModal">logout</a>
  
  <div class="topnav">
  <a class="active" href="/">Home</a>
  <a href="https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=189173&q=site:http%3A%2F%2Ffeeds.feedburner.com%2FTheHackersNews">News</a>
  <a href="dashboard">Dashboard</a>
  <a href="glossary">About</a>
</div>
    <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
    <title>Damn Vulnerable Flask Application: """ + CONFIG['app_name'] +"""</title>
    
    <body>
        <h1> Set of Vulnerabilities</h1>
        <h1> Just pick up one and start hacking.</h1>
        <div class="vertical-menu">
        <a href="/lookup">Do DNS lookup on address</a><br>
        <a href="/evaluate">Evaluate expression</a><br>
        <a href="/xml">Parse XML</a><br>
        <a href="/sayhi">Receive a personalised greeting</a><br></li>
        </div>
    </body>
    </html>
    """
@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('error.html', error=error)

@app.route('/evaluate', methods = ['POST', 'GET'])
#Code Injection
def evaluate():
    expression = None
    if request.method == 'POST':
        expression = request.form['expression']
    return """
    <html>
       <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
       <body>""" + "Result: " + (str(eval(expression)).replace('\n', '\n<br>')  if expression else "") + """
          <form action = "/evaluate" method = "POST">
             <h1> Hello Folks! Give us your problem. We will provide you the best mathematical solution. </h1>
             <p><h3>Enter expression to evaluate</h3></p>
             <p><input type = 'text' name = 'expression'/></p>
             <p><input type = 'submit' value = 'Evaluate'/></p>
          </form>
       </body>
       <a href="dashboard">Go back</a>
    </html>
    """
#os command Injection  
@app.route('/lookup', methods = ['POST', 'GET'])
def lookup():
    address = None
    if request.method == 'POST':
        address = request.form['address']
    return """
    <html>
    <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
       <body>""" + "Result:\n<br>\n" + (rp("nslookup " + address).replace('\n', '\n<br>')  if address else "") + """
          <form action = "/lookup" method = "POST">
             <h1> Hello Folks!Are you searching for ip address?Just write and search.</h1>
             <p><h3>Enter address to lookup</h3></p>
             <p><input type = 'text' name = 'address'/></p>
             <p><input type = 'submit' value = 'Lookup'/></p>
          </form>
       </body>
       <a href="dashboard">Go back</a>
    </html>
    """
#XXE    
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
    <title>xml</title
    <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
       <body><h1> Do you like to plays with markup?</h1>
       <h1> Give us your code we will design for you.</h1>
       """ + "Result:\n<br>\n" + cgi.escape(parsed_xml)  if parsed_xml else "" + """
          <form action = "/xml" method = "POST">
             <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
             <h1> Do you like to play with markup?</h1>
       <h1> Give us your code we will design for you.</h1>
             <p><h3>Enter xml to parse</h3></p>
             <textarea class="input" name="xml" cols="40" rows="5"></textarea>
             <p><input type = 'submit' value = 'Parse'/></p>
          </form>
       </body>
       <a href="dashboard">Go back</a>
    </html>
    """


# server side template injection
@app.route('/sayhi', methods = ['POST', 'GET'])
def sayhi():
   name = ''
   if request.method == 'POST':
      name = '<br>Hello %s!<br><br>' %(request.form['name'])

   template = """
   <html>
      <body>
         <link rel= "stylesheet" type= "text/css" href="/static/styles/board.css"">
         <form action = "/sayhi" method = "POST">
            <p><h3>Tell us your name and we want to send you greetings!</h3></p>
            <p><input type = 'text' name = 'name'/></p>
            <p><input type = 'submit' value = 'Submit'/></p>
         </form>
      %s
      </body>
      <a href="dashboard">Go back</a>
   </html>
   """ %(name)
   return render_template_string(template)

if __name__ == "__main__":
  app.debug = True
  db.create_all()
  app.run(host="0.0.0.0", port=8000)