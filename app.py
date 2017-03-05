from flask import Flask, render_template, request, url_for
import psycopg2
import os
import urllib.parse
from datetime import datetime
app = Flask(__name__)

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

@app.route('/install/')
def insta():
    conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
    cur = conn.cursor()
    cur.execute("CREATE TABLE mymsg (id serial PRIMARY KEY, name varchar, message varchar);")
    conn.commit()
    cur.close()
    conn.close()
    return "OK"
	
@app.route('/')
def form():
    return render_template('form_submit.html')

@app.route('/msg/', methods=['POST'])
def message_handler():
    myname=request.form['myname']
    mymsg=request.form['mymsg']
    conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
    cur = conn.cursor()
    cur.execute("INSERT INTO mymsg (name, message) VALUES (%s, %s)",(myname, mymsg))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('form_action.html', name=myname, msg=mymsg)
	
@app.route('/get')
def get_messages():
    conn = psycopg2.connect(database=url.path[1:],user=url.username,password=url.password,host=url.hostname,port=url.port)
    cur = conn.cursor()
    cur.execute("SELECT * FROM mymsg;")
    r = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('getall.html', r=r)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

