# nihonPy
## Tyler Freberg - https://www.linkedin.com/in/tfre
A Python program that functions as a Japanese <-> English dictionary with (simple) flashcard support.

### How It's Made:

**Language:** Python

**Libraries Used:** BeautifulSoup, urllib.request, requests, pykakasi, pynput, rich.progress, ast, sys, os, random

The program is comprised of a few main functions:
- **main_menu():** The main menu that everything revolves around. Calls the other funtions when a user states what they want to do.
- **word_def():** Performs a search for a user-supplied word. Uses BeautifulSoup to scrape the html of https://jisho.org.
- **sentence_find():** Similar to word_def(), but for sentences.
- **word_convert():** Converts a word to hiragana/romaji using pykakasi.
- **flash_create():** Creates a flash card and adds it to a user-supplied deck name.
- **flash_practice():** Let's the user practice created flashcard decks.

### Uses
- **Word Searching:** Users can either input a specified word or press **Enter** for a random word.
  - The word search function gives the user the word, hiragana and romaji readings, a definition, and sentences
    for the top result. The user can view more pages containing similar words' readings and definitions.
  - The random word option pulls a random english word from Github user deekayen's [list of 1000 most common English words.](https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt)
  - When entering a specified word, the user has the option to convert any kanji characters to hiragana. The benefit of this is
    that it can supply more results, but it is usually not recommended, as due to kanji having many different readings, the
    converted word may contain an incorrect reading. The user is warned about this when asked if they want to convert.
- **Flashcards:** The user can add a specific word to a deck with a name of their choosing.
  - Users can then practice created decks. Decks are located in the ./decks/ folder
### Considered Updates for Development in the Future
- add more options to the flashcard system
  - Management (deleting decks/words, renaming), Spaced Repetition System (SRS)
- kanji search
  - kanji readings, meanings, stroke order
- transition from a terminal interface to a graphical interface

### Troubles and Lessons Learned
Having little experience in web development, it can be difficult figuring out how to parse HTML data and get the data I need in a clean format.
This project has helped me learn how to do so more efficiently.

This is my first larger-scale project. This experience has taught me a lot about debugging, learning different ways to achieve desired results,
and overall creating a project that I am proud of.
