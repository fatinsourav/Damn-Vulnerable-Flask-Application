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
import sqlite3 as sql
from flask_cors import CORS,cross_origin
app = Flask (__name__)
app.secret_key = 'Harry Potter And The Deathly Hallows'

APP_NAME = 'Damn Vulnerable Flask Application'

CONFIG = {
    
    'app_name' : APP_NAME

}
@app.after_request 
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


def insertUser(username, email, password, contact):
    con = sql.connect("user.db")
    cur = con.cursor()
    phone = int(contact)
    query = ("""INSERT INTO USERS
             (username,email,password,contact)
             VALUES ('%s','%s','%s',%d)""" %
             (username, email, password, phone))
    cur.execute(query)
    con.commit()
    con.close()

def validUser(email, password):
    con = sql.connect("user.db")
    cur = con.cursor()
    query = ("""SELECT * FROM USERS
             where email = '%s' and password = '%s'
             """ %
             (email, password))
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    return data

@app.route('/signin/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        rd = validUser(request.form['email'], request.form['password'])
        if rd:
            return "Sucessful Login"
        else:
            return "UnSucessful login"
    else:
        return render_template('index2.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']
        insertUser(username, email, password, contact)
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

def rp(command):
    return popen(command).read()


  
@app.route('/dashboard')
def index():
    return """
    <html>
    <head><title>Damn Vulnerable Flask Application: """ + CONFIG['app_name'] +"""</title></head>
    <body>
        <p><h3>Bugs</h3></p>
        
        <a href="/cookie">Set and get cookie value</a><br>
        <a href="/lookup">Do DNS lookup on address</a><br>
        <a href="/evaluate">Evaluate expression</a><br>
        <a href="/xml">Parse XML</a><br>
        <a href="/config">View some config items</a><br>
        <a href="/sayhi">Receive a personalised greeting</a><br></li>
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
       <body>""" + "Result: " + (str(eval(expression)).replace('\n', '\n<br>')  if expression else "") + """
          <form action = "/evaluate" method = "POST">
             <p><h3>Enter expression to evaluate</h3></p>
             <p><input type = 'text' name = 'expression'/></p>
             <p><input type = 'submit' value = 'Evaluate'/></p>
          </form>
       </body>
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
       <body>""" + "Result:\n<br>\n" + (rp("nslookup " + address).replace('\n', '\n<br>')  if address else "") + """
          <form action = "/lookup" method = "POST">
             <p><h3>Enter address to lookup</h3></p>
             <p><input type = 'text' name = 'address'/></p>
             <p><input type = 'submit' value = 'Lookup'/></p>
          </form>
       </body>
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
       <body>""" + "Result:\n<br>\n" + cgi.escape(parsed_xml)  if parsed_xml else "" + """
          <form action = "/xml" method = "POST">
             <p><h3>Enter xml to parse</h3></p>
             <textarea class="input" name="xml" cols="40" rows="5"></textarea>
             <p><input type = 'submit' value = 'Parse'/></p>
          </form>
       </body>
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
         <form action = "/sayhi" method = "POST">
            <p><h3>What is your name?</h3></p>
            <p><input type = 'text' name = 'name'/></p>
            <p><input type = 'submit' value = 'Submit'/></p>
         </form>
      %s
      </body>
   </html>
   """ %(name)
   return render_template_string(template)

if __name__ == "__main__":
  app.debug = True
  app.run(host="0.0.0.0", port=8000)