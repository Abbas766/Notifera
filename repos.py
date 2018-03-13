import sys
import json
import argparse
import re
import requests
import issues
import watchlist

# Setting up a argument parser for command line interfacing
parser = argparse.ArgumentParser(description = 'Add or remove a repository from WatchList')
group =parser.add_mutually_exclusive_group()

# adding mandatory argument i.e. link
parser.add_argument('link', help = 'Link of the Github Repository')

# adding mutually exclusive arguments i.e. add or remove 
group.add_argument('-a','--add', help = 'Add the Github Repository to watchlist',action='store_true')
group.add_argument('-rm','--remove', help = 'Remove the Github Repository from watchlist',action ='store_true')

# Parsing the arguments
args = parser.parse_args()
repo_url = args.link

# Matching the parsed link for owner and repository name
regobj = re.match('https://github.com/([\w-]+)/([\w-]+).git',repo_url)    
if regobj==None:
	print('You entered an invalid url. Please try again.')
	sys.exit(0)
else:
	owner =regobj.group(1)
	repo_name =regobj.group(2)

# connecting to  NotiferaDB database
connection = watchlist.connectdb()
# Creating or connecting to watchlist table in NotiferaDB
watchlist.connectWatchList(connection)
# Creating or connecting to issues table in NotiferaDB
issues.connectIssues(connection)

if args.add or args.remove:
	# Requesting github api for repository data
	r = requests.get('https://api.github.com/repos/' +
    	              owner + '/' +
        	          repo_name)

	# parsing the data in json format
	data = json.loads(r.text or r.content)

	if args.add:
		values = []
		try:
			values.append(int(data['id']))
			values.append(data['name'])
			values.append(int(data['owner']['id']))
			values.append(data['owner']['login'])
			values.append(data['description'])
			values.append(data['issue_events_url'])
			values.append(data['issues_url'])
			values.append(int(data['has_issues']))  	#boolean value
			values.append(int(data['archived']))	   	#boolean value 
			values.append(int(data['open_issues_count']))
			values.append(int(data['open_issues']))
			# Checking if repository is archived
			if int(data['archived']):
				print("This repository has been marked 'ARCHIVED'.\nArchived repositories cannot be added to the watchlist")
				sys.exit(0)

			# adding repository to the watchlist
			watchlist.addRepo(connection,values)	
			# checking if repo has issues and adding them to issues table (if any).
			if int(data['has_issues']):
				issues.addNewRepoIssues(connection,data['owner']['login'],data['name'],int(data['id']))

		except Exception as e:
			print(e.message())
			print("No such repository exists.\nPlease Check the repository link or repository name.")	
				
	else:
		# removing repository (if exists) from watchlist
		watchlist.removeRepo(connection,repo_name)
		# removing issues of the repository (if any) from issues table
		issues.removeRepoIssues(connection,repo_name)

else:
	# add or remove caommand not passed 
	# simply checking for if repository exists in WatchList or not
	if watchlist.checkRepo(connection,repo_name):
		print("Repository already present in the watchist.")
	else:
		print("Repository not present in the watchlist.\nYou can add this repository using '-a' or '--add' command.")