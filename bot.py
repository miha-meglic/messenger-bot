import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# Start Selenium, log in and return driver
def start_bot():
	# Launch browser
	print('Launching Selenium')
	options = Options()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	time.sleep(1)
	# Open messenger
	print(f'Opening https://www.facebook.com/messages/t/{chatID}')
	driver.get(f'https://www.facebook.com/messages/t/{chatID}')
	time.sleep(1)
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
	messenger = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div/div/div[1]/div/iframe').get_attribute('src')
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
	ActionChains(driver).send_keys(message).send_keys(Keys.ESCAPE).send_keys(Keys.RETURN).perform()


# Environment and general parameters
load_dotenv()
email = os.getenv('EMAIL')
passw = os.getenv('PASSWORD')
text_hashes = list()

# ChatID for the chat to be used
chatID = '1275398675887743'

# Starts bot
driver = start_bot()

# Get messages and ignore them (so it doesn't reply to earlier messages)
get_messages()
print('Bot up and running...')

# Say hi to chat
print(f'\tBot started and connected')
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
				print(f'\tReplying to help from "{name}"')
				bot_send(f'[BOT] Commands: !ping, !whoami, !spam <message>')
			elif text == '!quit':
				print(f'\tBot shut down by "{name}"')
				bot_send('[BOT] Bye')
				time.sleep(1)
				driver.quit()
				driver = None
				break
			elif text == '!ping':
				print(f'\tReplying to ping from "{name}"')
				bot_send('[BOT] Hello :)')
			elif text == '!whoami':
				print(f'\tReplying to whoami from "{name}"')
				bot_send(f'[BOT] You\'re {name}')
			elif text.find('!spam') == 0:
				print(f'\tSpamming "{o_text[6:]}" for "{name}"')
				for i in range(9):
					bot_send(f'[BOT] {o_text[6:]}')
			
			# Random ticks
			if text.find('gej') != -1 or text.find('gay') != -1:
				print(f'\tReplying to "{name}", who said "gej"')
				bot_send(f'[BOT] {name} je gej')
			if text.find('roza') != -1:
				print(f'\tReplying to "{name}", who said "roza"')
				bot_send(f'[BOT] Joštova najljubša barva je roza')
	time.sleep(2)
