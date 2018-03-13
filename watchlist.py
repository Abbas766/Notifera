import sqlite3


def connectdb():
	# Setting the connection to the database 'NotiferaDB.db'
	try:
		connection = sqlite3.connect('NotiferaDB.db')
	except Exception:
		print("Database connection Failed !...")
		return None
	return connection

def connectWatchList(connection):
	# Getting the cursor
	cursor = connection.cursor()

	# Creating a Table to store data only if table does not exist
	cursor.execute("CREATE TABLE IF NOT EXISTS watchlist\
					(	repoid INTEGER PRIMARY KEY NOT NULL,\
						reponame varchar(400) NOT NULL,\
						ownerid INTEGER,\
						ownername varchar(400),\
						description TEXT,\
						issue_events_url TEXT,\
						issues_url TEXT,\
						has_issues BOOLEAN,\
						archived BOOLEAN,\
						open_issues_count INTEGER,\
						open_issues INTEGER\
					)")


def addRepo(connection,values):
	# Getting the cursor
	cursor = connection.cursor()
	values = tuple(values)
	sql = "INSERT INTO watchlist VALUES(%d,\"%s\",%d,\"%s\",\"%s\",\"%s\",\"%s\",%d,%d,%d,%d)"%values

	try:
		# Insert the values 
		cursor.execute(sql)
		connection.commit()
		print('Repository added')
		
	except sqlite3.IntegrityError as e:  # handling redundancy error
		print("Repository already present in watchlist.") 
	

def removeRepo(connection,repo_name):
	# Getting the cursor
	cursor = connection.cursor()

	# Checking if repository exists in database
	if checkRepo(connection,repo_name):
		# if exists then delete
		cursor.execute("DELETE FROM watchlist WHERE reponame='"+repo_name+"'")
		connection.commit()
		print('Repository removed')
	else:
		print("Repository not found in the watchlist.")	
	
	

def checkRepo(connection,repo_name):
	# Getting the cursor
	cursor = connection.cursor()
	
	cursor.execute("SELECT * FROM watchlist WHERE reponame='"+repo_name+"'")
	f = cursor.fetchone()
	return True if f else False
