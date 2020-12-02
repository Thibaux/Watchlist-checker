import requests
from bs4 import BeautifulSoup
import smtplib
import time
import operator
import secrets
import pandas as pd

eye_classics = []
eye_restored_unseen = []
eye_premiers = []
eye_all_films = []
titles = []
films_eye = []
found_films = []

def EyeAllfilms():
	def EyeClassics():
		global eye_classics
		global eye_all_films
		EyeFilmNames = list();
		url = 'https://www.eyefilm.nl/en/themes/eye-classics#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		for filmName in filmNames:
			filmName = filmName.text
			eye_classics += [filmName]

		eye_all_films += eye_classics

	def EyeRestored_Unseen():
		global eye_all_films
		global eye_restored_unseen
		EyeFilmNames = list();
		url = 'https://www.eyefilm.nl/en/themes/restored-unseen#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		for filmName in filmNames:
			filmName = filmName.text
			eye_restored_unseen += [filmName]

		eye_all_films += eye_restored_unseen

	def EyePremiers():
		global eye_premiers
		global eye_all_films
		EyeFilmNames = list();
		url = 'https://www.eyefilm.nl/en/themes/premieres#full-program'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.11 Safari/537.36'}
		page = requests.get(url, headers = headers)
		soup = BeautifulSoup(page.content, 'html.parser')

		filmNames = soup.find_all('h4', {'class': 'h3 full-program-title'})
		FilmDirectors = soup.find_all('div', {'class': 'full-program-subtitle'})

		for filmName in filmNames:
			filmName = filmName.text
			eye_premiers += [filmName]

		eye_all_films += eye_premiers

	EyeClassics()
	EyeRestored_Unseen()
	EyePremiers()
EyeAllfilms()

def GetWatchlist():
	global df
	global head
	df = pd.read_csv(r'watchlist.csv')
GetWatchlist()

def FilterFilms():
	global titles
	global films_eye
	global found_films
	def NoMatchesFound():
		not_found_msg = f"""

	Sorry man, er draaien geen films van je watchlist bij Eye.
		"""
		print(not_found_msg)

	for row in df.itertuples():
		title = row[2]
		title = title.lower()
		titles += [title]

	for i in range(len(eye_all_films)):
		eye_all_films[i] = eye_all_films[i].lower()
		films_eye += [eye_all_films[i]]

	check = any(item in films_eye for item in titles)

	if check is True:
		for i in films_eye:
			while i in titles:
				found_films.append(i)
				break

	if check is False:
		for i in films_eye:
			NoMatchesFound()
			break

FilterFilms()


def SendMail():
	global found_films
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()

	server.login(secrets.sender, secrets.password)

	subject = f"Dit zijn de films die nu draaien bij Eye"
	body = f"""
	{found_films}
	"""
	msg = f"Subject: {subject}\n\n{body}"

	server.sendmail(
		secrets.sender,
		secrets.receiver,
		msg
	)

	print('send')
	server.quit()

SendMail()

def interval():
	time_wait = 60
	EyeAllfilms()
	print(f'Ff wachten pik, nog {time_wait} minuten')
	time.sleep(time_wait * 60)

# if __name__ == '__main__':
# 	while True:
# 		interval()



