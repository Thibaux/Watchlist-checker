import requests
from bs4 import BeautifulSoup
import smtplib
import time
import operator
import secrets
import pandas as pd

bioscopen = list()
eye_all_films = []
titles = []
films_eye = []
all_films = []
found_films = []

# Function to retrieve all the films that the cinema Eye is playing at the moment
def EyeAllfilms():

	# Append this cinema to the list of cinema's
	bioscopen.append("Eye") 

	# Get the Eye classics that are on display now
	def EyeClassics():
		global eye_all_films
		eye_classics = []
		EyeFilmNames = list();

		url = 'https://www.eyefilm.nl/en/themes/eye-classics#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		# Find the film names and assing them to a variable
		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		# Find the film diractors and assing them to a variable
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		# Append the films to a classics array first
		for filmName in filmNames:
			filmName = filmName.text
			eye_classics += [filmName]

		# Append the films to the total list of films playing at eye
		eye_all_films += eye_classics

	# Get the Eye restord & unseen that are on display now
	def EyeRestored_Unseen():
		global eye_all_films
		eye_restored_unseen = []
		EyeFilmNames = list();

		url = 'https://www.eyefilm.nl/en/themes/restored-unseen#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		# Find the film names and assing them to a variable
		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		# Find the film diractors and assing them to a variable
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		# Append the films to a classics array first
		for filmName in filmNames:
			filmName = filmName.text
			eye_restored_unseen += [filmName]

		# Append the films to the total list of films playing at eye
		eye_all_films += eye_restored_unseen

	# Get the Eye premiers that are on display now
	def EyePremiers():
		global eye_all_films
		eye_premiers = []
		EyeFilmNames = list();

		url = 'https://www.eyefilm.nl/en/themes/premieres#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		# Find the film names and assing them to a variable
		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		# Find the film diractors and assing them to a variable
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		# Append the films to a classics array first
		for filmName in filmNames:
			filmName = filmName.text
			eye_premiers += [filmName]

		# Append the films to the total list of films playing at eye
		eye_all_films += eye_premiers

	# Call al the funtions
	EyeClassics()
	EyeRestored_Unseen()
	EyePremiers()
EyeAllfilms()

# Retrieve the films from my watchlist with pandas
def GetWatchlist():
	global df
	global head
	df = pd.read_csv(r'watchlist.csv')
GetWatchlist()

# Loop through all the arrays so that they can be matched to each other
def FilterFilms():
	global titles
	global films_eye
	global found_films
	global all_films

	# Loop through the watchlist
	for row in df.itertuples():
		title = row[2]
		title = title.lower()
		titles += [title]

	# Loop through the eye films
	for i in range(len(eye_all_films)):
		eye_all_films[i] = eye_all_films[i].lower()
		films_eye += [eye_all_films[i]]

	# Add the films from all the cinema's to a vaiable
	all_films = films_eye

FilterFilms()

# Checks for matches in lists
def check():
	global titles
	global all_films
	global found_films
	global bioscopen

	# Add a comma to every cinema entry
	bioscopen = ", ".join(bioscopen)

	# Check if there are films playing that are in my watchlist aswell
	check = any(item in all_films for item in titles)

	# If that is the case add these films to a list 
	# Show user that film are found
	# Call the send mail function
	# End the script
	if check is True:
		for i in all_films:
			while i in titles:
				found_films.append(i)
				break
		print(f"""

	Jaa! Er draaien films van je watchlist bij {bioscopen}.
			""")
		SendMail()
		exit()

	# If that is not the case show the user
	if check is False:
		for i in all_films:
			print(f"""
	Sorry man, er draaien geen films van je watchlist bij {bioscopen}.
			""")
			break


def SendMail():
	global found_films

	# Setup mailing server
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	# Login to my mail with hidden credentials
	server.login(secrets.sender, secrets.password)

	# Add content to the mail
	subject = f"Dit zijn de films die nu draaien bij Eye"
	body = f"""
	{found_films}
	"""
	msg = f"Subject: {subject}\n\n{body}"

	# Send the mail
	server.sendmail(
		secrets.sender,
		secrets.receiver,
		msg
	)

	# Show the user that the mail has been send
	print(f"""
	Mail send!
	""")
	server.quit()

# Function to keep the script running if check is false
def interval():
	# Time in hours
	time_wait = 1
	check()
	# Show user that the script will run again
	print(f"""
	We proberen het over {time_wait} uur weer, oke?
		""")
	time.sleep(time_wait * 3600)

if __name__ == '__main__':
	while True:
		interval()