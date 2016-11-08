# README #

###CS322 Project 6: Mongo Database###
###Author: Marc Leppold###

##Project Notes

The sixth project in CS322. A simple MongoDB database that displays text memos sorted by date. Users can input their own memos with custom text and a custom date into a form, which will be sent to the database and displayed accordingly after pressing 'submit'. Users can delete memos in the same process: by entering the text of the memo you want to delete into the text field and toggling the 'remove' radio button, then pressing 'submit'.

Requires admin/user credentials to create and access the database - the admin credentials must be supplied by the user, the user credentials are provided with certain releases of this program but must be supplied by the user otherwise. Contains a few sample programs - db_trial.py and destroy_db.py, which don't directly aid the functionality of the program but give the user options, namely the ability to test a few sample inputs easily and the ability to delete the database they've created.

Contains tests with nose for checking if the datetime handling and database insertion/deletion are correct. Run them with nosetests after configuring.

### USAGE ###

Execute the following commands
```
git clone https://github.com/zenranda/proj6-mongod InstallDirectory
cd InstallDirectory
. configure
. env/bin/activate
python3 create_db.py
make run
```
where InstallDirectory is the directory you cloned the files to. Running create_db makes a database matching the specs in the user config file and with the admin credentials, it's required in order for this project to run.

While it's running, enter
```
HOST:PORT/index
```
into an internet browser, where HOST is the host IP of the computer the program is running on and PORT is the port it's configured to (default 5000).
Please note that this program requires a constant internet connection in order to recieve and send database info.
