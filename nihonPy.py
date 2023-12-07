#!/usr/bin/env python3

import ast
import os
import random
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import pykakasi as pk
from pynput import keyboard
from pynput.keyboard import Key, Listener
from rich.progress import Progress
global defcount


# the main menu
# self explanatory
def main_menu():
	
	# when main_menu is called again after the initial call, it automatically inputs "^[" from the esc key
	# the three lines below press the backspace button once to remove this to avoid any issues after call 1 
	kb = keyboard.Controller()
	kb.press(Key.backspace)
	kb.release(Key.backspace)


	os.system('clear')
	print("\033[1mWelcome to nihonPy!\033[0m\nA Python Japanese Dictionary\n\nChoose an option below\n\n\033[1mCtrl:\033[0m Search a Word\t\033[1mAlt:\033[0m Practice and Manage Flashcards\n\nPress \033[1mHome\033[0m to view the bug log.\n\nPress \033[1mEsc\033[0m to Exit")
	
	def on_press(key):
		global ex
		ex = False
		if key == Key.home:
			bug_log()
		if key == Key.esc:
			ex = True
			return False
		if key ==  Key.ctrl:
			return  False
		if key == Key.alt:
			os.system('clear')
			print("\033[1mFlashcard Manager\033[0m\n")
			print("Here, you can practice flashcards and add words to decks.\n\n\033[1mCtrl\033[0m: Practice a Deck\t\033[1mAlt\033[0m: Add a Card\n\nPress \033[1mEsc\033[0m to return to the main menu")
			
			def on_press(key):
				if key == Key.ctrl:
					flash_practice()
				if key == Key.alt:
					flash_create()

			with Listener(on_press=on_press) as listener:
				listener.join()

	with Listener(on_press=on_press) as listener:
		listener.join()

	if ex == True:
		os.system('clear')
		exit()

	# clear the screen and prompt the user for a word
	os.system('clear')
	user_word = (input("Enter a word to search or press Enter for a random word: ")).strip("^[")
	os.system('clear')

	# checks if user requested a random word
	if user_word == '':
		user_word = random_word()

	# checks the following:
	# 1. Can a word be converted? The try statement checks if it is an ascii character (in other words alphabetical)
	# 2. Does the user want it to be converted to hiragana from kanji? This is not always the best option, as the
	#    chance of an irrelevant word showing up goes up when not specifying kanji
	try:
		user_word.encode(encoding='utf-8').decode('ascii')
	except:
		print("\033[1mWould you like your word converted to hiragana?\033[0m\n\nThis will show more words with similar sounds but different kanji.")
		print(f"Example: {user_word} becomes {word_convert(user_word, 'hira')}")
		print("\nNote: May provide incorrect conversions. Not recommended if looking for info on specific words.\n\nPress \033[1mShift\033[0m to convert.\nPress \033[1mEnter\033[0m to continue without conversion.")
		
		def on_press(key):
			global flag
			flag = 0
			if key == key.shift:
				flag =  1
				return False
			if key == key.enter:
				return False
		with Listener(on_press=on_press) as listener:
			listener.join()
		if flag == 1:
			user_word = word_convert(user_word, 'hira')
	else:
		global flag
		flag = 0
		user_word


	# perform the word search
	os.system('clear')
	if flag == 1:
		print("Word converted.")
	print(f"Searching for the word '{user_word}'...")
	wordlist = word_def(user_word)
	os.system('clear')

	# if wordlist is empty, then no definition was found
	if len(wordlist) == 0:
		print("Word not found.")
		main_menu()

	# this is the top and most likely best definition
	# showing only one at first also helps avoid crowding the screen with too many options
	maindef = wordlist[0:1]

	# if the user would like to search for more words/definitions, this list contains all others
	otherwords = wordlist[1:int(len(wordlist))]

	print(f"\033[1mSearched Word: {user_word}\033[0m")

	# formatting and printing info to screen
	defcount = 1
	for item in maindef:
		for word, defi in item.items():
			sentences = sentence_find(word)
			os.system('clear')
			print(f"\033[1mSearched Word: {user_word}\033[0m")
			print_word(word, defi, defcount)
			if len(sentences) > 0:
				print("\t\033[1mSentences:\033[0m")
				i = 1
				for item in sentences[0:3]:
					for sentence, translation in item.items():
						print(f"\t{i}.{sentence}\n\t{translation}\n")
						i += 1
			else:
				print("\033[1mNo Sentences Found\033[0m")
			if len(otherwords) == 0:
				print("\033[1mNo Other Words Found\033[0m\n")
			defcount += 1
	
	# limiting page to 10 words for organization purposes.
	# If otherwords is less than 10, then there is only one more page,
	# and we don't have to worry about splitting it into multiple pages.
	if len(otherwords) > 0 and len(otherwords)<=10:
		print("Press \033[1mShift\033[0m for more definitions\nPress \033[1mEsc\033[0m to return to the main menu")
		
		def on_press(key):
			if key == Key.shift:
				os.system('clear')
				print(f"\033[1mSearched Word: {user_word}\033[0m")
			
				defcount = 2
				for item in otherwords:
					for word, defi in item.items():
						print_word(word, defi, defcount)
						defcount += 1
				print("Press \033[1mEsc\033[0m to return to the main menu")
				if key == Key.esc:
					main_menu()
		
			if key == Key.esc:
				main_menu()

		with Listener(on_press=on_press) as listener:
			listener.join()

	# if otherwords is more than 10, split it into two pages.
	# jisho.org seems to have a max of 20 items per page, so we don't have to
	# worry about more than 20 items total. So we will have at max 3 pages.
	if len(otherwords) > 10:
		firsthalf = []
		secondhalf = []

		splitter = 0
		for item in otherwords:
			if splitter <10:
				firsthalf.append(item)
			else:
				secondhalf.append(item)
			splitter += 1
			
		print("Press \033[1mShift\033[0m for more definitions\nPress \033[1mEsc\033[0m to return to the main menu")
		
		def on_press(key):
			if key == Key.shift:
				os.system('clear')
				print(f"\033[1mSearched Word: {user_word}\033[0m")
			
				defcount = 2
				for item in firsthalf:
					for word, defi in item.items():
						print_word(word, defi, defcount)
						defcount += 1
				return False							
			if key == Key.esc:
				main_menu()


		with Listener(on_press=on_press) as listener:
			listener.join()


		print("Press \033[1mShift\033[0m for more definitions\nPress \033[1mEsc\033[0m to return to the main menu")
		
		def on_press(key):
			if key == Key.shift:
				os.system('clear')
				print(f"\033[1mSearched Word: {user_word}\033[0m")
			
				defcount = 12
				for item in secondhalf:
					for word, defi in item.items():
						print_word(word, defi, defcount)
						defcount += 1
				print("Press \033[1mEsc\033[0m to return to the main menu")

			if key == Key.esc:
				main_menu()
		
		with Listener(on_press=on_press) as listener:
			listener.join()

	else:
		print("Press \033[1mEsc\033[0m to return to the main menu")
		
		def on_press(key):
			if key == Key.esc:
				main_menu()

		with Listener(on_press=on_press) as listener:
			listener.join()

	keyboard.Listener.stop()
	return


# how-to-use information gathered from official Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Scrapes HTML of https://jisho.org/ for word information
def word_def(word):
	# processing bar to let user know things are working...
	with Progress(transient=True) as progress:

		print("Loading words...")
		progress.add_task("", total = None)

		word_list = []

		# get HTML data
		html = requests.get('https://jisho.org/search/'+word)

		# make it readable
		soup = bs(html.content, 'html.parser')
		results = soup.find(id = 'primary')

		# sort info into a list of dicts
		for item in results.find_all('div', class_='concept_light clearfix'):
			word_bank = {}
			word = (item.find('span', class_='text')).text.strip()
			if item.find_all('span', class_='meaning-meaning'):
				defi = (item.find('span', class_='meaning-meaning')).text.strip()

			word_bank[word] = defi
			word_list.append(word_bank)

		return word_list


# how-to-use information gathered from official Beautiful Soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# scrapes HTML of https://jisho.org/ for sentence information
def sentence_find(word):
	# processing bar to let user know things are working...
	with Progress(transient=True) as progress:
	
		print("Searching for sentences...")
		progress.add_task("", total = None)

		sentences = []

		# get HTML data
		html = requests.get("https://jisho.org/search/"+word+"%20%23sentences")

		#make it readable
		soup = bs(html.content, 'html.parser')
		results = soup.find(id = 'secondary')

		# remove unnecessary/annoying class items for clean sentence storage
		for span in results.find_all('span', class_='furigana'):
			span.decompose()
		for span in results.find_all('span', class_='inline_copyright jreibun'):
			span.decompose()
		for span in results.find_all('span', class_='inline_copyright'):
			span.decompose()

		# sort info into a list of dicts
		for item in results.find_all('li', class_='entry sentence clearfix'):
			sent_dict = {}
			sentence = (item.find('ul', class_='japanese_sentence japanese japanese_gothic clearfix')).text.strip()
			translation = (item.find('div', class_='english_sentence clearfix')).text.strip()
			sent_dict[sentence] = translation
			sentences.append(sent_dict)

		return sentences


# Ocassionally, when a word is inputted by the user in kanji, it limits the words thrown back to the user.
# This converts any potential kanji words to hiragana or hepburn romanization.
# This can also be used to display hiragana and romaji pronunciation for kanji.
# Unfortunately, this library is not perfect, most likely due to each kanji having many different readings.
def word_convert(word, base):
	# how-to-use information gathered from official pykakasi documentation: https://pykakasi.readthedocs.io/en/latest/
	kks = pk.kakasi()
	converted = ""
	word_con = kks.convert(word)

	# provided base determines if conversion is hiragana or romaji
	if base == 'hira':
		for item in word_con:
			converted += item['hira']
	if base ==  'hepburn':
		for item in word_con:
			converted += item['hepburn']

	return  converted


# print word in an organized format
def print_word(word, defi, count):
	hiragana = ""
	romaji = ""
	hiragana = word_convert(word, 'hira')
	romaji = word_convert(word, 'hepburn')
	print(f"\033[1m{count}. {word}\n\tHiragana:\033[0m {hiragana}\n\t\033[1mRomaji:\033[0m {romaji}\n\t\033[1mDefinition:\033[0m {defi}\n")


# pulls a random word from https://github.com/deekayen's list of 1000 most common US English words.
# I tried to find lists of Japanese words online, but they had a lot of strange outliers.
# Luckily, jisho.org supports searching with English words, so this isn't an issue. 
def random_word():
	# processing bar to let user know things are working...
	with Progress(transient=True) as progress:
	
		print("Choosing a random word...")
		progress.add_task("", total = None)

		with urllib.request.urlopen("https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt") as req:
			data = (req.read().decode("utf-8")).split()

		# pick a random number, use that number as an index of data to select a random word
		num = random.randrange(1000)
		new_word = data[num]
		return new_word


# Lets a user add a word to a specified deck.
# This is a very basic flashcard system at the moment. I plan to develop it further down the road.
def flash_create(*args):
	os.system('clear')
	
	# this is used to check if the word the user supplied worked or not
	if args:
		for ar in args:
			word_err = ar
	else:
		word_err = 0

	print("\033[1mFlashcard Manager\033[0m\n")

	print("Here, you can practice flashcards and add words to decks.\n")

	print("\033[1mDecks\033[0m")
	
	deck_files = os.listdir("decks")
	for file in deck_files:
		if file.endswith(".deck"):
			#file = file.strip(".deck")
			print(file[:-5], end=" ")
	print("\n")

	# if word_err is 1, that means that flash_create() was called again with an argument of 1, meaning a word wasn't found in the search.
	if word_err == 1:
		deck_name = input("Word not found.\nEnter a deck name: ")
	else:
		deck_name = input("\nEnter a deck name: ")
	print ("\033[A                             \033[A")
	word = input("Enter a word to add: ")
	word_card = {}


	print ("\033[A                             \033[A")
	wordlist = word_def(word)

	if len(wordlist) == 0:
		flash_create(1)

	# currently, it only grabs the first definition.
	# Most of the time, this is sufficient.
	# This is to avoid stuffing the decks full of
	# unnecessary cards
	for word, defi in wordlist[0].items():
		word_card[word] = defi

	# create a deck file in ./decks
	path = "decks/"+deck_name+".deck"

	# write out each word as a dictionary on separate lines
	# tried to use json at first, but json doesn't seem to play
	# well with appending
	with open(path, "a+") as outfile:
		if str(word_card) not in outfile:
			print(str(word_card), file=outfile)

	# tells the user the deck location and
	# allows them to add another word
	print ("\033[A                             \033[A")
	print ("\033[A                             \033[A")
	print(f"Card added to deck: decks/{deck_name}.deck\n\nPress \033[1mAlt\033[0m to add another word\nPress \033[1mEsc\033[0m to return to the main menu")
	
	def on_press(key):
		if key == Key.alt:
			flash_create()
		if key == Key.esc:
			main_menu()
	with Listener(on_press=on_press) as listener:
		listener.join()


# lets the user practice created dcks
def  flash_practice(*args):

	# checks if specified deck exists
	if args:
		for ar in args:
			deck_err = ar
	else:
		deck_err = 0

	os.system('clear')
	print("\033[1mFlashcard Manager\033[0m\n")

	print("Here, you can practice flashcards and add words to decks.\n")

	print("\033[1mDecks\033[0m")
	
	deck_files = os.listdir("decks")
	for file in deck_files:
		if file.endswith(".deck"):
			#file = file.strip(".deck")
			print(file[:-5], end=" ")
	print("\n")
	
	# if word_err is 1, that means that flash_practice() was called again with an argument of 1, meaning the specified deck doesn't exist
	if deck_err == 1:
		deck_name = input("Deck not found. Enter a deck name to practice: ")
	else:
		deck_name = input("Enter a deck name to practice: ")
	
	# searches for deck file in ./decks
	os.system('clear')
	path = "decks/"+deck_name+".deck"

	if os.path.isfile(path):
		data = (open(path, 'r')).readlines()
	else:
		flash_practice(1)	

	# prints the cards
	for line in data:
		# converts line from string to dictionary
		line = ast.literal_eval(line)
		for word in line:
			print("\033[1mFlashcard Manager\033[0m\n")
			print("Front of card:")
			print("--------------------\n")
			print(f"    {word}")
			print("\n--------------------")
			print("Back of card:")
			print("--------------------\n\n\n")
			print("--------------------")
			print("\nPress \033[1mCtrl\033[0m to advance")
			
			def on_press(key):
				if key == Key.ctrl:
					os.system('clear')
					print("\033[1mFlashcard Manager\033[0m\n")
					print("Front of card:")
					print("--------------------\n")
					print(f"    {word}")
					print("\n--------------------")
					print("Back of card:")
					print("--------------------\n")
					print(f"{line[word]}")
					print("\n--------------------")
					print("\nPress \033[1mCtrl\033[0m to advance")

					def on_press(key):
						if key == Key.ctrl:
							return False
						else:
							return True

					with Listener(on_press=on_press) as listener:
						listener.join()
				
				return False

			with Listener(on_press=on_press) as listener:
				listener.join()

			os.system('clear')
	print("\033[1mFlashcard Manager\033[0m\n")
	print("Front of card:")
	print("--------------------\n")
	print("   Deck finished!   ")
	print("\n--------------------\n")
	print("Press \033[1mAlt\033[0m to practice a new deck\nPress \033[1mEsc\033[0m to return to the main menu")
	
	def on_press(key):
		if key == Key.alt:
			flash_practice()
		if key == Key.esc:
			main_menu()

	with Listener(on_press=on_press) as listener:
		listener.join()


# loads bug_log.txt
def bug_log():
	os.system('clear')
	with open("bug_log.txt", "r") as infile:
		data = infile.readlines()

	for line in data:
		print(line, end="")

	print("\n\nPress \033[1mEsc\033[0m to return to the main menu")
	
	def on_press(key):
		if key == Key.esc:
			main_menu()

	with Listener(on_press=on_press) as listener:
		listener.join()


if __name__ == '__main__':
	main_menu()