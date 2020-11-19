import time
import os
import random
import csv
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests

# Terminal color definitions
class col:
	reset = '\033[0m'
	red='\033[31m'
	green='\033[32m'
	orange='\033[33m'
	blue='\033[34m'
	purple='\033[35m'
	cyan='\033[36m'
	lightgrey='\033[37m'
	darkgrey='\033[90m'
	lightred='\033[91m'
	lightgreen='\033[92m'
	yellow='\033[93m'
	lightblue='\033[94m'
	pink='\033[95m'
	lightcyan='\033[96m'

# Start Selenium, log in and return driver
def start_bot():
	# Launch browser
	print('Launching Selenium')
	# options = Options()
	# options.add_argument('--headless')
	# driver = webdriver.Firefox(options=options)
	driver = webdriver.Firefox()
	time.sleep(1)
	# Open messenger
	print(f'Opening https://www.facebook.com/messages/t/{chatID}')
	driver.get(f'https://www.facebook.com/messages/t/{chatID}')
	time.sleep(1)
	# Accept cookies
	print("Accepting cookies")
	accept_bnt = driver.find_element_by_xpath('//*[@data-cookiebanner="accept_button"]')
	accept_bnt.click()
	# Login
	print(f'Logging in as {email}')
	username = driver.find_element_by_xpath('//*[@id="email"]')
	password = driver.find_element_by_xpath('//*[@id="pass"]')
	login = driver.find_element_by_xpath('//*[@id="loginbutton"]')
	username.send_keys(email)
	password.send_keys(passw)
	login.click()
	time.sleep(2)
	# Redirect to iframe src
	messenger = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/iframe').get_attribute('src')
	# messenger = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[1]/div/iframe').get_attribute('src')
	print('Redirecting to messenger iframe')
	driver.get(messenger)
	time.sleep(2)
	# Returns the driver
	return driver

# Get member list
def get_members():
	ret = list()
	for member in driver.find_elements_by_class_name('_8slc'):
		ret.append(member.text)
	return ret

# Get NEW messages from messenger
def get_messages():
	ret = list()
	# Cycle through message groups
	for mes_group in driver.find_elements_by_class_name('_41ud'):
		name = ''
		try:
			name = mes_group.find_element_by_xpath('h5').text
		except:
			try:
				name = mes_group.find_element_by_class_name('_4k7a').text
				name = name[:name.find(' replied')]
			except: continue
		# Get texts (if not already seen)
		texts = list()
		for text in mes_group.find_elements_by_class_name('_aok'):
			if text not in text_hashes:
				text_hashes.append(text)
				texts.append(text.text.replace('\n', ' '))
		# Add text to return list
		if texts:
			ret.append((name, texts))
	# Return messages
	return ret

# Send a message to messenger
def bot_send(message):
	message = message.split('\n')
	action = ActionChains(driver)
	for line in message:
		action.send_keys(line).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT)
	action.send_keys(Keys.BACK_SPACE).send_keys(Keys.ESCAPE).send_keys(Keys.RETURN).perform()

# Retrieve latest SARS-CoV-2 (COVID-19) data for Slovenia
def get_covid_stats():
	# Retrieve data from gov.si
	data = list(csv.DictReader(requests.get('https://www.gov.si/teme/koronavirus-sars-cov-2/element/67900/izvoz.csv').text.splitlines()))[0]
	# Parse data
	data = {
		'date': datetime.strptime(data['Datum'], '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y'),  # Date of data update
		'tested': int(data['Opravljeni testi']),  # People newly tested
		'positive': int(data['Pozitivne osebe']),  # People newly tested positive
		'hospitalized': int(data['Hospitalizirane osebe']),  # People currently hospitalized
		'icu': int(data['Osebe na intenzivni negi']),  # People currently on intensive care
		'released': int(data['Odpuščeni iz bolnišnice']),  # People newly released from hospital
		'died': int(data['Umrli'])  # New deaths
	}
	# Return data
	return data

# Get formated local time
def get_time():
	return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Environment and general parameters
load_dotenv()
email = os.getenv('EMAIL')
passw = os.getenv('PASSWORD')
text_hashes = list()

# ChatID for the chat to be used
# chatID = '1275398675887743'
chatID = input('Enter Chat ID: ')


# Magic 8-ball responses
m8 = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes – definitely', 'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy, try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again', 'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']

# Starts bot
driver = start_bot()

# Get messages and ignore them (so it doesn't reply to earlier messages)
get_messages()
print('Bot up and running...')
print('-' * 60)

# Say hi to chat
print(f'[{get_time()}] Bot {col.red}started and connected{col.reset}')
bot_send('[BOT] Hi :P')

# Check every two seconds
while True:
	# Exit loop if driver doesn't exist
	if not driver:
		break
	# Get new messages
	for (name, texts) in get_messages():
		for text in texts:
			# Do not reply to yourself
			if text.find('[BOT]') != -1:
				continue
			
			# Answer to bot stuff
			o_text = text
			text = text.lower()
			if text == '!help':
				print(f'[{get_time()}] Replying to {col.cyan}help{col.reset} from {col.green}"{name}"{col.reset}')
				bot_send(f'[BOT] Commands: !ping, !whoami, !spam <message>, !question <question>, !covid')
			elif text == '!quit':
				print(f'[{get_time()}] Bot {col.red}shut down{col.reset} by {col.green}"{name}"{col.reset}')
				bot_send('[BOT] Bye')
				time.sleep(1)
				driver.quit()
				driver = None
				break
			elif text == '!ping':
				print(f'[{get_time()}] Replying to {col.cyan}ping{col.reset} from {col.green}"{name}"{col.reset}')
				bot_send('[BOT] Pong :)')
			elif text == '!whoami':
				print(f'[{get_time()}] Replying to {col.cyan}whoami{col.reset} from {col.green}"{name}"{col.reset}')
				bot_send(f'[BOT] You\'re {name}')
			elif text.find('!spam') == 0:
				print(f'[{get_time()}] {col.cyan}Spamming "{o_text[6:]}"{col.reset} for {col.green}"{name}"{col.reset}')
				for i in range(5):
					bot_send(f'[BOT] {o_text[6:]}')
			elif text.find('!question') == 0:
				answer = m8[random.randrange(len(m8))]
				print(f'[{get_time()}] {col.cyan}Answering{col.reset} "{answer}" to "{o_text[10:]}" for {col.green}"{name}"{col.reset}')
				bot_send(f'[BOT] {answer}')
			elif text.find('!covid-19') == 0 or text.find('covid') != -1:
				print(f'[{get_time()}] Replying {col.cyan}SARS-CoV-2 stats{col.reset} for {col.green}"{name}"{col.reset}')
				stats = get_covid_stats()
				bot_send(f'[BOT] COVID fun fact\n{stats["date"]}\nTestirani: {stats["tested"]}\nPozitivni: {stats["positive"]} ({(float(stats["positive"]) / stats["tested"] * 100):.2f}%)\nUmrli: {stats["died"]}')
			
			# Random ticks
			if text.find('gej') != -1 or text.find('gay') != -1:
				print(f'[{get_time()}] Replying to {col.green}"{name}"{col.reset}, who {col.pink}said "gej"{col.reset}')
				bot_send(f'[BOT] {name} je gej')
			if text.find('roza') != -1:
				print(f'[{get_time()}] Replying to {col.green}"{name}"{col.reset}, who {col.pink}said "roza"{col.reset}')
				bot_send(f'[BOT] Joštova najljubša barva je roza')
	time.sleep(2)
