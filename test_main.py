####
#Tests our server
###
import flask_main
import arrow

# Mongo database
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated
    base_size = collection.count() #current size of the db, for comparison later

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)    

    
def test_dates():
    assert(flask_main.humanize_arrow_date(arrow.utcnow()) == "Today") 
    assert(flask_main.humanize_arrow_date(arrow.utcnow().replace(days=+7)) == "in 7 days")
    assert(flask_main.humanize_arrow_date(arrow.utcnow().replace(years=+7)) == "in a year")
    assert(flask_main.humanize_arrow_date(arrow.utcnow().replace(days=-1, hours=+4, minutes=+49)) == 'Yesterday')

def test_insertion_and_removal():
    flask_main.add_memo(collection, {"type" : "dated_memo", "date" : arrow.get(utcnow()), "text" : "The first entry." })
    flask_main.add_memo(collection, {"type" : "dated_memo", "date" : arrow.get(utcnow().replace(days=+19), "text" : "The second entry." })
    flask_main.add_memo(collection, {"type" : "dated_memo", "date" : arrow.get(utcnow().replace(days=+1, minutes=+9), "text" : "The third and final entry." })
    assert(collection.count() == (base_size+3))
    flask_main.remove_memo(collection, "The second entry.")
    assert(collection.count() == (base_size+2))
    flask_main.remove_memo(collection, "The first entry.")
    assert(collection.count() == (base_size+1))
    flask_main.add_memo(collection, {"type" : "dated_memo", "date" : arrow.get(utcnow().replace(days=+100, minutes=+2), "text" : "The fourth and seriously final entry." })
    assert(collection.count() == (base_size+2))
    flask_main.remove_memo(collection, "The third and final entry.")
    flask_main.remove_memo(collection, "The fourth and seriously final entry.")
    assert(collection.count() == base_size)