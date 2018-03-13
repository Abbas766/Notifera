import sqlite3
import requests
import json
# def connectdb():
# 	# Setting the connection to the database 'NotiferaDB.db'
# 	try:
# 		connection = sqlite3.connect('NotiferaDB.db')
# 	except Exception:
# 		print("Database connection Failed !...")
# 		return None
# 	return connection


def connectIssues(connection):
	# Getting the cursor
	cursor = connection.cursor()

	# Creating (if it does not exists) the issues table
	cursor.execute("CREATE TABLE IF NOT EXISTS issues\
					(	issueid INTEGER PRIMARY KEY NOT NULL,\
					 	title TEXT,\
					 	reponame varchar(500) NOT NULL,\
					 	repoid INTEGER NOT NULL,\
					 	issuenumber INTEGER NOT NULL,\
					 	body TEXT,\
					 	state varchar(200),\
					 	created_at varchar(200),\
					 	updated_at varchar(200)\
					)")
def addNewRepoIssues(connection,owner,reponame,repoid):
	# Getting the cursor
	cursor = connection.cursor()

	# Requesting github api for repository issues data
	r = requests.get('https://api.github.com/repos/' +
    	              owner + '/' +
        	          reponame +'/issues')

	# parsing the data in json format
	data = json.loads(r.text or r.content)

	for issue in data:
		if issue["state"]=="closed":
			continue
		else:
			print(list(issue.keys()))
			#print(issue["issue"]["title"])
			sql = "INSERT INTO issues VALUES(%d,\"%s\",\"%s\",%d,%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"%(
					int(issue["id"]),
					issue["issue"]["title"],
					reponame,
					repoid,
					int(issue["issue"]["number"]),
					issue["issue"]["body"],
					issue["state"],
					issue["issue"]["created_at"],
					issue["issue"]["updated_at"]
					)
			print(sql)
			try:
				# Insert the values 
				cursor.execute(sql)
				connection.commit()
				
			except sqlite3.IntegrityError as e:  # handling redundancy error
				continue

def removeRepoIssues(connection,reponame):
	# Getting the cursor
	cursor = connection.cursor()
	
	cursor.execute("DELETE FROM issues WHERE reponame='"+reponame+"'")
	connection.commit()
	print('Issues removed')

