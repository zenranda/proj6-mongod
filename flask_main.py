"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import g
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times
import datetime

# Mongo database
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/")
@app.route('/index', methods =['POST'])
def addremove_Memo():
    if request.form['options'] == "Add":
   	 record = { "type" : "dated_memo",
        	    "date" : arrow.get(request.form['memoDate'], "YYYY/M/D", tzinfo=tz.tzlocal()).naive,
                    "text" : request.form['memoMake']}
   	 collection.insert(record)
    if request.form['options'] == "Remove":
        db = request.form['memoMake']
        collection.remove( { "text" :  db } )

    return index()


@app.route("/")
@app.route("/index")
def index():
  app.logger.debug("Main page entry")
  g.memos = get_memos()
  for memo in g.memos: 
      app.logger.debug("Memo: " + str(memo))
  return flask.render_template('index.html')





@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    try:
        now = arrow.utcnow().to('local').replace(hour=1, minute=0, second=0, microsecond=0) #the current date, but not time
        then = arrow.get(date)

        if then.tzinfo==None:
            then.to('local').replace(hour=1, minute=0, second=0, microsecond=0, tzinfo=tz.tzlocal()) #the current date, in proper tz
        else:
            then.replace(hour=1,minute=0, second=0, microsecond=0) #if the tz was read as local (from html form)

        tomorrow = now.replace(days=+1)                           #cases for rounding humanized dates
        yesterday = now.replace(days=-1)   
        
        print("Then is " + str(then) + " Now is " + str(now))
        if then.date() == now.date():
            human = "Today"
        elif then.date() == tomorrow.date():
            human = "Tomorrow"
        elif then.date() == yesterday.date():
            human = "Yesterday"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"

    except: 
        human = date
    return human

############
#
# Functions for testing purposes
#
############

def add_memo(db, mem):
   """
   Adds a memo to our collection
   """
    db.insert(mem)

def remove_memo(db, txt):
   """
   Removes a memo containing the text
   """
   db.remove( { "text" : txt } ) 


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ):
        record['date'] = arrow.get(record['date']).isoformat()
        del record['_id']
        records.append(record)
    return sorted(records, key=lambda entry : entry['date'])   #sorts by date


if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")

    
