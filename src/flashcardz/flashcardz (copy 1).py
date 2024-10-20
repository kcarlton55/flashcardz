#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed July 13, 2024

@author: Ken Carlton, kencarlton55@gmail.com

A simple flashcards program used to, among other things, learn another
language.  Flash cards are saved in a local file.  The file has the form:

word1 | definition1 | date | viewed | tally
word2 | definition2 | date | viewed | tally
           ...
wordN | definitionN | date | viewed | tally

Date is the date that a particular card was created.  Viewed is the number of
times that the card has been viewed.  Tally is the number of times the user
correctly knew the definition of a word without a miss. Tally is reset to zero
anytime the user did not rememember the definition.

Once the maximum tally value has been reached (default is 10), the word is
removed from the card set.  To run the program, run the go() function.
The go() function shuffles the cards before presenting cards to the user.

This program is meant to be run using python's interactive command-line
terminal (i.e. read-eval-print loop (REPL) terminal).  This comes standard when
python is installed on your PC.
"""

#import pdb  # use with pdb.set_trace()
from datetime import date, datetime
import random
import time
from pathlib import Path
import csv
from difflib import get_close_matches
import sys
import os
import ast
import re
import webbrowser
import readline  # https://docs.python.org/3/library/readline.html
import code
import atexit


__version__ = '0.1.0'   # PEP 440 - describes versions
delimiter = '|'      # pipe symbol
substitute = ';'     # if when file saved, save any pipe symbols as semicolons


def _remains_at(setting):
    """
    This is subfunction called by _setpathname(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    s = _settings[setting]
    print('\nProgram setting remains at:')
    print(f'    _settings["{setting}"] = {s}')


def _changed_to(setting):
    """
    This is subfunction called by _setpathname(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    s = _settings[setting]
    print('\nProgram setting changed to:')
    print(f'    _settings["{setting}"] = {s}')
    _write_settingsfn()


def _currently_at(setting):
    """
    This is subfunction called by _setpathname(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    s = _settings[setting]
    print('\nSetting is currently:')
    print(f'    _settings["{setting}"] =  {s}')


def _setabort():
    """
    Change the setting named "abort" to True or False.  If set to True then
    any results, such as tallys, will NOT be recorded when go() is run.
    If False, then results will be recorded.
    """
    global _settings
    print(_setabort.__doc__)
    _currently_at('abort')
    abort = input('\n    abort (Enter nothing for no change) = ').strip()
    if abort == "1" or abort == 'True':
        abort = True
    elif abort == "0" or abort == 'False':
        abort = False
    else:
        abort = None
    if _settings['abort'] == abort:
        _remains_at('abort')
    elif abort == False or abort == True:
        _settings['abort'] = abort
        _changed_to('abort')
    else:
        print('\nTrue or False are the only valid responses')
        _remains_at('abort')


def _settallypenalty():
    """
    Change the setting named "tallypenalty".  Each time you correctly know the
    definition of a card's word, the tally for that word is increased by one.
    If the word was missed (you didn't know the definition) then the tally is
    reduced by the value of "tallypenalty".

    For example, if tallypenalty = 3, and the tally for a word is 8, then
    the tally will be set to 5 if you missed the word.

    If tallypenalty = 0, then a deduction never occurs.  If tallypenalty is
    greater than or equal to the setting for "maxtally", then tally will
    be set back to zero when a word is missed.
    """
    global _settings
    print(_settallypenalty.__doc__)
    _currently_at('tallypenalty')
    tallypenalty = input('\n    tallypenalty (Enter nothing for no change) = ')
    if tallypenalty.strip():
        tallypenalty = int(tallypenalty)
    if isinstance(tallypenalty, int) and tallypenalty != int(_settings['tallypenalty']):
        _settings['tallypenalty'] = abs(int(tallypenalty))
        _changed_to('tallypenalty')
    else:
        _remains_at('tallypenalty')


def _setmaxtally():
    '''
    Each time the user knows correctly the definition of a word, the tally
    for that word is incremented by one.  When the tally reaches the value of
    "maxtally", the card is removed from the deck.
    '''
    global _settings
    print(_setmaxtally.__doc__)
    _currently_at('maxtally')
    maxtally = input('\n    maxtally (Enter nothing for no change) = ')
    if maxtally.strip():
        maxtally = abs(int(maxtally))
    if isinstance(maxtally, int) and maxtally != int(_settings['maxtally']):
        _settings['maxtally'] = maxtally
        _changed_to('maxtally')
    else:
        _remains_at('maxtally')


def _setdateformat():
    """
    Info on date_formats can be found at https://strftime.org/

    date_format %x represents "Locale’s appropriate date representation".
    With %x, in the US the date will look like 09/17/24.
    Options to consider: %m-%d-%Y (09-17-2024), %Y-%m-%d (2024-09-17)
                         %m-%d-%y (09-17-24), %m/%d/%y (09/17/24).

    Once a card's file has a particular format established within it, it is
    best not to change it.  If changed, when the data file is opened, and the
    format of the date does not match the current setting, that date will be
    erased and replaced with the current date.
    """
    global _settings
    print(_setdateformat.__doc__)
    _currently_at('date_format')
    current_date = datetime.now()
    date_format = input('\n    date_format (Enter nothing for no change) = ')
    if date_format.strip() and date_format.strip('"') != _settings['date_format']:
        _settings['date_format'] = date_format.strip('"')
        _changed_to('date_format')
        current_date_formatted = current_date.strftime(_settings['date_format'])
        print(f'\nExammple: {current_date_formatted}')
    else:
        _remains_at('date_format')


def _setpathname():
    '''
    Set the pathname (filename prepended by a path) for where your set of cards is
    located.  If the file doesn't exist at the location you specify, it will be created.
    '''
    global _settings
    print(_setpathname.__doc__)
    print(f'(current working directory is: {Path().cwd()})')

    _currently_at('pathname')
    print("\nEnter pathname for new or existing file (e.g. C:\\mypath\\myfile.txt)")
    userinput = input(r'    Pathname (Enter nothing for no change) = ').strip()
    fn = Path(userinput)
    fn_resolved = fn.resolve()
    current_fn = Path(_settings['pathname']).resolve()
    if userinput and  fn_resolved.is_dir():
        print(f'\npathname cannot be a directory. You tried to create {fn_resolved}')
        _remains_at('pathname')
    elif userinput and not fn_resolved.parent.exists():
        print(f'\nParent directory {fn_resolved.parent} does not exist.')
        print('Withont a parent directory your file cannont be created.')
        _remains_at('pathname')
    elif  userinput and fn_resolved == current_fn:
        print("You didn't change the pathname.")
        _remains_at('pathname')
    elif userinput and fn_resolved.exists():
        print('\nFile already exists.  Will use that file.')
        _settings['pathname'] = str(fn_resolved)
        _changed_to('pathname')
    elif (userinput and not fn_resolved.exists()) or (userinput and fn_resolved.exists()):
        _settings['pathname'] = str(fn_resolved)
        _changed_to('pathname')
    else:
        _remains_at('pathname')


def settings():
    """Adjust program's settings to tailer the behavior to fit your needs.
    """
    global _settings
    print(settings.__doc__)
    print(f"(Settings are saved in file {_get_settingsfn()}.")
    print('If this file is erased, once flashcardz is rerun, file will be recreated')
    print('with settings reset to defaults.)')
    print('\nCurrent settngs are:')
    for key, value in _settings.items():
        print(f'    {key}: {value}')
    chgkey = input('\nSetting to change (Enter nothing for no change): ')
    print()
    chgkey = str(chgkey).strip()
    if chgkey and chgkey not in _settings.keys():
        print(f'\n"{chgkey}" not found')
        closest = get_close_matches(chgkey, _settings.keys(), 1)
        if closest:
            print(f'Perhaps you meant this?: {closest[0]}')
        else:
            print('\nAvailable choices:')
            for k in _settings.keys():
                print(f'    {k}')
    if chgkey == 'pathname':
        _setpathname()
    elif chgkey == 'maxtally':
        _setmaxtally()
    elif chgkey == 'abort':
        _setabort()
    elif chgkey == 'tallypenalty':
        _settallypenalty()
    elif chgkey == 'date_format':
        _setdateformat()


def functions():
    '''    Functions are:  add(), cards(), delete(), functions(), go() and
    settings().

    The primary functions are add(), cards(), and go().

    Enter help(functionname) to learn more about a function.  Enter
    print(__doc__) to see overview docs.  Instructions on how to use flashcardz
    can be found at https://github.com/kcarlton55/flashcardz

    Examples
    --------

    >>> help(add)

    >>> help(go)
    '''
    print(f'\n{functions.__doc__}')


def add(word, definition):
    ''' Add a new card to your card deck.  This function will automatically
    open the file that contains your deck of cards, add your new card, and then
    save the updated data to your file.

    Parameters
    ----------
    word : string
        New word to add to the deck of cards.  (A string is text surrounded
        by quotation marks, e.g. "house (noun)"; though triple quotes make
        working with the comannd line window easier, i.e. """house (noun)""")
    definition : string
        Definition of the word.  Surround your string (i.e. text) with
        quotation marks.  If your string is multiline, surround your string by
        triple quotes, e.g.:
        """ a building that serves as living quarters for one or a few
        families; a shelter, refuge."""

        URL links can be included within a description.  URL links must have
        the form [some text](a url).  For example, a description may look like:

        """blah blah blah [connect to google](https://www.google.com/) blah
        blah [John 3:16](https://www.biblegateway.com/passage/?search=john%203%3A16&version=NKJV)
        blah blah blah [youtube](https://www.youtube.com/)"""

        See help(go) and help(cards) to see how to activate links.

    Examples
    --------

    >>> add("taza nf", "(bol pequeño con asa)  cup n, mug n")


    #  When go() is run, word and desription will show as:
    #
    #    taza nf
    #
    #    (bol con asa)  cup n, mug n


    >>> add("""correr vi""",
        """(moverse deprisa)
           run vi
           (rush) get a move on v expr
           go quickly, go fast vi + adv""")


    #  When go() is run, word and desription will show as:
    #
    #    correr vi
    #
    #    (moverse deprisa)
    #         run vi
    #         (rush) get a move on v expr
    #         go quickly, go fast vi + adv
    #
    #  Note: make sure to put a closing ) at the end.
    #  Note: \\n, and \\t are special character combinations that you can use.
    #  \\n is a "new line" character; i.e. a new line will be entered into
    #  your text.  \\t is a "tab" character.  It will enter a tab space.


    >>> w = "correr vi"

    >>> d = """(moverse deprisa)
    \\t run vi
    \\t (rush) get a move on v expr
    \\t go quickly, go fast vi + adv"""

    >>> print(d)   # shows the description and the effect of \\t

    >>> add(w, d)


    #  This is another way to achieve the same result as the previous example.
    #
    #  Tip 1: If the definition you entered isn't to your satifaction, push the
    #  up key so that the add function you previously entered reappears; then
    #  edit it.  (When you use the add function, if you use the EXACT same word
    #  (i.e. exact same characters, spaces in exactly the same locations, etc.),
    #  the new defintion that you enter will replace the old definition.)
    #
    #  Tip 2: When pasting a word and/or its defintion, start with add(""" and
    #  then paste.  To move the cursor within your pasted text, use the key
    #  board's arrow keys.
    '''
    if word and definition and type(word) == str and type(definition) == str:
        _cards = _open()
        today = date.today()
        today = today.strftime(_settings['date_format'])
        word = word.replace(delimiter, substitute)
        definition = definition.replace(delimiter, substitute)
        for i, x in enumerate(_cards):
            # word from _cards (x[0]), all white space removed, & lower case
            x0 = ''.join(x[0].split()).lower()
            # new word from user (word), all white space removed, & lower case
            word0 = ''.join(word.split()).lower()
            if x0 == word0:  # if word already in _cards, delete it to replace with new
                _cards.pop(i)
                _cards.append([word, definition, x[2], x[3], x[4]])
                break
        else:
            _cards.append([word, definition, today, 0, 0])
        print(f'\n{word}\n\n{definition}\n')
        print('Number of cards now at: ', len(_cards))
        _save(_cards)
    else:
        print('\nError at add function.  Here is an example of how to do it:\n')
        print('add("pill", "a small round mass of solid medicine to be swallowed whole.")')


def delete(number=None):
    '''
    Delete a card from the deck.  Use words(), head(), or tail() to see the
    number associated with a particular card.  Knowing that number allows you
    to delete that card.

    Parameters
    ----------
    number : int, optional
        The number of the card you want to delete. If no number is provided,
        you will be asked for it.  The default is None.

    Examples
    --------
    # If you do not supply a number, you will be asked for it.
    delete()

    # Delete card number 5
    delete(5)

    '''
    _cards = _open()
    if not number == None:
        number = abs(int(float(number)))
    if number == None:
        print('Card number to delete?  (Run function cards() (or head() or tail())')
        print('to see what word corresponds to what number.)\n')
        number = input('Number: ')
    if isinstance(number, str):
        number = abs(int(float(number)))
    if number < len(_cards):
        print(f'\nCard {number} is: {_cards[number][0]}.\n')
        confirm = input(f'Delete card {number}? [Y/n): ')
        if confirm.lower() not in ['n', 'no']:
            print(f'\nCard {number} deleted ({_cards[number][0]})\n')
            _cards.pop(number)
            print('Number of cards now at: ', len(_cards))
            _save(_cards)
        else:
            print(f'Card {number} not deleted.')
    else:
        print(f"Card number {number} doesn't exist.")


def _save(_cards):
    '''
    Save your cards to a file.  File format is text, meaning that it can be
    opened with a text editor.  Furthermore, the file is structured in csv
    format, meaning that it can opened with Microsoft Excel.  Note that if you
    open the file with Excel, Excel may ask what delimiter the csv file uses.
    The delimiter is the vertical bar character, |.

    Since the delimiter is a |, i.e. the character used separate column
    fields, | characters are not allowed in text that you enter for a word or
    its definition.

    Parameters
    ----------
    _cards : list
        list of cards that has the format:
        cards = [['word1', 'definition1', 'date', 'viewed', 'tally'],
                 ['word2', 'definition2', 'date', 'viewed', 'tally'],
                   ...,
                 ['wordN', 'definitionN', 'date', 'viewed', 'tally']]

    Elements of the list are strings execept for 'viewed' (no. of times
    viewed) and 'tally' which are integers.

    '''
    if ('pathname' not in _settings or _settings['pathname'] == None
            or _settings['pathname'] == ""):
        _setpathname()
    fields = ['word', 'definition', 'date', 'viewed', 'tally']
    try:
        fn = Path(_settings['pathname'])
        with open(fn, 'w', newline='', encoding='utf-8', errors='replace') as csvfile:  # w/o newline='', blank lines inserted with MS Windows
            csvwriter = csv.writer(csvfile, delimiter=delimiter)
            csvwriter.writerow(fields)
            csvwriter.writerows(_cards)
    except Exception as e:
        msg = ("Error at _save function:\n\n"
               "Unable to save flashcardz data file.\n"
               "Perhaps you have it open with another program?\n  "
               + str(e))
        print(msg)


def _open():
    '''
    Open the pathname specified in flashcardz' _settings, then read its
    contents.  Convert those contents to a python list object.  The file that
    is opened is specfied in flashcardz' _settings at '_settings["pathname"]'

    Returns
    -------
    _cards : list
        List of words and their difinitions; included is the create date,
        how many times a word has been viewed, and the tally for that word.
        (tally: number of times a user has correctly known the defintion of a
         word.)

    '''
    today = date.today().strftime(_settings['date_format'])
    try:
        if ('pathname' not in _settings or _settings['pathname'] == None
                or _settings['pathname'] == ""):
            _setpathname()

        fn = Path(_settings['pathname'])

        _cards = []
        with open(fn, 'r', encoding='utf-8', errors='replace') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter)
            for _card in csvreader:
                ln = len(_card)
                if 1 < ln < 5:
                    del _card[2:]
                    _card.append(today)
                    _card.append('0')
                    _card.append('0')
                elif ln == 1:
                    print('\nSomething is wrong with your data file.  At least one line in the file contains\n'
                           'data that would fill only one field, and not multiple fields, i.e. the word and\n'
                           'description fields.  The most likely reason for this is that the file was not\n'
                           'saved in a csv file format suitable for the flachcardz program.   The file\n'
                           'should be a csv file that uses a pipe/vertical bar character, |, as a delimiter.')
                    sys.exit()
                try:    # is date in a legitimate format?
                    legit_date = bool(datetime.strptime(_card[2], _settings['date_format']))
                except ValueError:
                    legit_date = False
                if not legit_date:
                    _card[2] = today
                if not _card[3].isnumeric():
                    _card[3] = '0'
                if not _card[4].isnumeric():
                    _card[4] = '0'
                if not _card[0] == 'word':
                    _cards.append(_card)
    except Exception as e:
        msg = ('Error within function named "_open function".\n'
               + str(e))
        print(msg)
    return _cards


def cards(cmd=True, i=None):
    """From the cards' data file, show a list of all words with, or without,
    their defintions.

    Parameters
    ----------
    cmd (optional) : bool | int | list | range
        if cmd == True (the default); show all words, but without their
            definitions.
        if cmd == False; show all words and their definitions.
        if type(cmd) == int (i.e. integer); at position "int" show word and its
            definition. (do "cards()" to see integers that correspond to words)
        if type(cmd) == list; where list is a list of ints, at locations of
            ints, show words and definitions.
        if type(cmd) == range; show words and definitions starting at the
            beginning int value in range, up to and not including the last
            int value.

    i : int
        URL links (see add() function) can exists in the description field of
        for a given word.  If so, then i represents the 1st, 2nd, etc. link.
        Entering that number will cause a web browser to open that link.
        Note: this only works if "cmd" is an integer.

    Returns
    -------
    None.

    Examples
    --------
    # Show a list of all words
    >>> cards()

    # Show all words and their defintions
    >>> cards(False)

    # Show the word and its definition at postion 8 in the data file.
    # (To see postion numbers, issue the "cards()" command.)
    >>> cards(8)

    # Open a web browser and with it open the 2nd link shown in the
    # description for card 8.  (Links are surrounded by brackets, []).
    >>> cards(8, 2)

    # Show word and its defintion at postions 5, 7 and 10:
    >>> cards([5, 7, 10])

    # Show words and their defintions starting and position 5 and ending at
    # postion 12
    >>> cards(range(5, 13))

    """
    try:
        _cards = _open()
        separator = 21*'-'
        if type(cmd) == int and i == None:
            j = cmd
            _card = _cards[j]
            desc = _hide_urls(_card[1])
            print(f'\n{_card[0]}\n\n{desc}')
        elif type(cmd) == int and isinstance(i, int) and i < 0:
            j = cmd
            _card = _cards[j]
            desc = _card[1]
            print(f'\n{_card[0]}\n\n{desc}')
        elif type(cmd) == int and isinstance(i, str) and i == '-0':
            j = cmd
            _card = _cards[j]
            desc = _card[1]
            print(f'\n{_card[0]}\n\n{desc}')
        elif type(cmd) == int and isinstance(i, int):
            j = cmd
            _card = _cards[j]
            webbrowser.open(_url_at(_card[1], i))
        elif type(cmd) == list:
            lst = cmd
            for j in lst:
                _card = _cards[j]
                desc = _hide_urls(_card[1])
                text2 = (f'{separator} {_card[2]}, viewed: {_card[3]}, tally: {_card[4]} {separator}\n' +
                            f'{j}. {_card[0]}\n' + f'{desc}')
                print(text2)
        elif type(cmd) == range:
            rng = cmd
            for j in rng:
                _card = _cards[j]
                desc = _hide_urls(_card[1])
                text2 = (f'{separator} {_card[2]}, viewed: {_card[3]}, tally: {_card[4]} {separator}\n' +
                            f'{j}. {_card[0]}\n' + f'{desc}')
                print(text2)
        else:
            for j, _card in enumerate(_cards):
                desc = _hide_urls(_card[1])
                text1 = f'{j}. {_card[0] : <30} (tally: {_card[4] : >})'
                text2 = (f'{separator} {_card[2]}, viewed: {_card[3]}, tally: {_card[4]} {separator}\n' +
                         f'{j}. {_card[0]}\n' + f'{desc}')
                print(text1) if (cmd == 1 or cmd == True) else print(text2)
    except:
        print('Error at function named cards.')
        print('    Data file nonexistant or corrupt?  Was csv file saved with | as delimiter?')


def go(shuffle=True):
    '''
    First the deck of cards in shuffled.  Then one by one each card is shown
    to the user.  First the word is shown.  The user looks at the word and
    tries to figure out what the word means.  Then the user hits any key.
    The defintion is then shown.  The user is asked if he/she knew what the
    word meant.  If he/she answere yes, then the tally is incremented
    by one.  (Tally is the number of times the user knew what the word means.)
    If the user didn't know, the the tally for that word is reset to zero
    (or another value defined in the program's settings).

    Once a max tally is reached (determined by the program's settings), the
    card is removed from the deck.

    When go() is run, the file that contains the card deck is opened.  After
    all the cards are viewed by the user, the updated card deck is saved.  If
    the user aborts before go() is finished, results are not saved.

    Parameters
    ----------
    shuffle : bool, optional
        Shuffle the deck. The default is True.

    Examples
    --------
    # Don't shuffle the deck (False or 0 results in a non-suffle)
    >>> go(False)

    # Shuffle the deck (True or 1, or enter no argument)
    >>> go()

    '''
    print('\nEach word, followed by its definition, will be shown.  After a word is shown,')
    print("try to figure out its meaning.  Then press the Enter key to show the word's")
    print('definition.  The program will then ask "Meaning known? (Y/n/i/a/q)".')
    print('Respond with one of these answers:')
    print("    " + 75*"—")
    print("     Y or the Enter key = you knew the definition")
    print("     n = you did not know the definition")
    print("     i = input an integer instead of i.  That is, enter 1, 2, 3, etc..  i is")
    print("         the 1st, 2nd, 3rd, etc. url link within a description; that is, if the")
    print("         link exists.  Links are enclosed in brackets, [].  Enter a negative")
    print("         number if you wish to see the url appear in the description.")
    if _settings['abort'] == True:
        abort = True
        print('     (Note: _settings["abort"] = True.  RESULTS WILL NOT BE SAVED!)')
    else:
        print("     a = abort recording of results when go() completes its run")
    print("     q = cancel showing cards")
    print("    " + 75*"—")

    print()
    ans1 = input("Press any key to start. ")
    if ans1 and (ans1[0].lower() == 'q' or ans1[0].lower() == 'e'):
        return
    print("\nHere we go!")

    _cards = _open()
    index_list = [i for i in range(0, len(_cards))]
    if shuffle == True:
        print("\nShuffling cards ", end='')
        for i in range(15):
            print(">", end='')
            time.sleep(.08)
        print()
        index_list = sorted(index_list, key=lambda x: random.random())

    number = 0
    number_of_cards = len(_cards)
    abort = False
    unwanted = []
    missed = []
    print()
    correcttext = ('Meaning known? (Y/n/i/q) ' if _settings['abort']
                   else 'Meaning known? (Y/n/i/a/q) ')

    for k in index_list:
        _cards[k][3] = int(_cards[k][3]) + 1   # _cards[k][3] is "viewed"
        number += 1
        loop = True
        flag = True
        hide_url = True
        while loop:
            print(25*'-' + ' tally: ' + str(_cards[k][4]) + ' ' + 25*'-')
            print(f'{number} of {number_of_cards}.  {_cards[k][0]}')  # _cards[k][0] is "word"
            if flag:  # pause after word shown, but pause only once.
                flag = False
                ans0 = input()
                if ans0 and (ans0[0].lower() == 'q' or ans0[0].lower() == 'e'):
                    return
            if hide_url:
                desc = _hide_urls(_cards[k][1])  # _cards[k][1] is "description"
            else:
                desc = _cards[k][1]
            print(f'{desc}\n')
            ans = input(correcttext)

            if ans and ans.isnumeric():
                hide_url = True
                webbrowser.open(_url_at(_cards[k][1], int(ans)))
            elif ans and ans[0] == '-' and ans[1:] and ans[1:].isnumeric():
                hide_url = False
            elif ans and ans[0].lower() == 'i':
                hide_url = True
                print('\n    Entering "i" is inappropriate.  Instead enter 1, 2, 3, etc., depending on')
                print('    which URL link is shown in brackets, [], that you wish to activate; i.e. the')
                print('    1st, 2nd, 3rd.\n')
            elif ans and (ans[0].lower() == 'q' or ans[0].lower() == 'e'):
                return
            elif ans and ans[0].lower() == 'a' and abort == False:
                abort = True
                hide_url = True
                correcttext = 'Correctly answered? (Y/n/i/q) '
                print("    " + 75*"—")
                print('     Results will NOT be recorded when go() completes its run')
                print("    " + 75*"—")
            elif ans and ans[0].lower() == 'a' and abort == True:
                hide_url = True
                abort = False
                correcttext = 'Correctly answered? (Y/n/i/a/q) '
                print("    " + 75*"—")
                print('     Results WILL be recorded when go() completes its run')
                print("    " + 75*"—")
            elif ans and ans[0].lower() == 'n':
                print()
                _cards[k][4] = max(0,  _settings['maxtally'] - _settings['tallypenalty'])
                missed.append(_cards[k])
                loop = False
            elif ans and ans[0].lower() == 'y':
                print()
                _cards[k][4] = int(_cards[k][4]) + 1    # _cards[k][4] is "tally"
                if _cards[k][4] >= _settings['maxtally']:
                    unwanted.append(k)
                loop = False
            else:
                print()
                _cards[k][4] = int(_cards[k][4]) + 1
                if _cards[k][4] >= _settings['maxtally']:
                    unwanted.append(k)
                loop = False
    print("\n             === The End ===")

    if unwanted:
        unwanted = sorted(unwanted)
        print('\n\n' + 50*'_')
        if not abort:
            print(
                'Congradulations!  Max tally reached on the following.  Cards removed: \n')
        else:
            print('Congradulations!  Max tally reached on the following: \n')
        # [::-1] reverses the list in order to remove latter elements first.
        for ele in unwanted[::-1]:
            # ele is an element of the _cards list
            print(f'    {_cards[ele][0]}')
            del _cards[ele]
        print()
        if not abort:
            print(f'\nNumber of cards is now {len(_cards)}\n')

    if missed:
        print('\n\n' + 50*'_')
        percent_correct = str(
            int(100 * (len(_cards) - len(missed))/len(_cards)))
        if int(percent_correct) >= 80:
            print(f'{percent_correct}% answered correctly!')
        else:
            print(f'{percent_correct}% answered correctly')
        print('These are the words you missed: \n')
        for m in missed:
            for i, c in enumerate( _cards):
                if c[0] == m[0]:
                    break
            print(f'{i}. {m[0]}')
    else:
        print('\n\n' + 50*'_')
        if len(_cards) == 0:
            print('Card deck is empty.  Please add data.')
        else:
            print('100% of list answered correctly!')


    if not abort:
        _save(_cards)


def _get_settingsfn():
    '''Get the pathname (path and name) to store user's settings.  The file
    will be named _settings.txt.  The pathname will be vary depending on who's
    logged in and what os is being used.  Pathname will look like:
    C:\\Users\\Ken\\AppData\\Local\\flashcardz\\_settings.txt.  On a linux
    os, will look like: /home/Ken/.flashcardz/_settings.txt

    If the pathname does not already exists, it will be created, and default
    settings will be inserted into the file, i.e.
    {"maxtally": "10", "abort": "False",  ...}
    '''

    if sys.platform[:3] == 'win':  # if a Window operating system being used.
        datadir = os.getenv('LOCALAPPDATA')
        path = os.path.join(datadir, 'flashcardz')
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        settingsfn = os.path.join(datadir, 'flashcardz', '_settings.txt')

    elif sys.platform[:3] == 'lin':  # if a Linux operating system being used.
        homedir = os.path.expanduser('~')
        path = os.path.join(homedir, '.flashcardz')
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        settingsfn = os.path.join(homedir, '.flashcardz', '_settings.txt')

    else:
        printStr = ('At method "get_configfn", a suitable path was not found to\n'
                    'create file settings.txt.  Notify the programmer of this error.')
        print(printStr)
        return ""

    _bool = os.path.exists(settingsfn)

    if not _bool or (_bool and os.path.getsize(settingsfn) == 0):
        fn_2_suggest = _suggest_fn()
        print('\n\n It appears this is your first time running this program.  A file\n'
              ' name needs to be established in which a new card deck will be\n'
              ' started.  Please provide a pathname; i.e. filename prepended with a path.')
        print('\n')
        fn = input(fr'    file name ({fn_2_suggest}): ')
        fn = fn.strip()

        if not fn:
            fn = str(fn_2_suggest)
            print('\nProgram setting pathname set to:')
            print(f'    _settings["[pathname"] = {fn}')
        with open(settingsfn, 'w') as file:
            file.write(f'{{"pathname": "{fn}", "maxtally": "10", ' +
                       '"tallypenalty": "10", ' +
                       '"date_format": "%x", "abort": "False"}')
    return settingsfn


def _read_settingsfn():
    global _settings
    try:
        settingsfn = _get_settingsfn()
        with open(settingsfn, 'r') as file:
            x = file.read().replace('\\', '/')
        _settings = ast.literal_eval(x)
        _settings['maxtally'] = int(_settings['maxtally'])
        _settings['tallypenalty'] = int(_settings['tallypenalty'])
    except Exception as e:
        msg = ("\n\n\n !!! Error at _read_settingsfn() function:\n"
               " !!! Unable to open settings.txt file which allows the program to remember user\n"
               " !!! settings.  To fix, try deleting the file that contains these settings.\n"
               " !!! When this program sees that this file is missing, it will be recreated with\n"
               " !!! with default settings.  This file is located at:\n !!!\n !!! ")
        msg += _get_settingsfn()
        print(msg)


def _write_settingsfn():
    try:
        settingsfn = _get_settingsfn()
        with open(settingsfn, 'w') as file:
            file.write(str(_settings))
    except Exception as e:
        msg = ("\nError at _write_settingsfn() function:\n\n"
               "Unable to save flashcardz data file.\n"
               "Perhaps you have it open with another program?\n  "
               + str(e))
        print(msg)


def _suggest_fn():
    home_dir = Path.home()
    doc_dir = Path.home().joinpath('Documents')
    if doc_dir.is_dir():
        return doc_dir / 'flashcardz.txt'
    elif home_dir.is_dir():
        return home_dir / 'flashcardz.txt'
    else:
        pass


def _hide_urls(text):
    """Look for subtext in text that looks like
    [connect to google](https://www.google.com/)
    and then remmove the "(https://www.google.com/)" portion.  That is,
    look for pattern [some text](a url) and remove the (a url).

    Parameters
    ----------
    text : string
        Text to search for the pattern

    Returns
    -------
    Returns the same text less the URL and the parenthesis that
    inclosed that URL.
    """
    tuples = re.findall(r'(\[.+?\])(\s*\(.+?\))', text)
    for url in tuples:
        text = text.replace(url[1], '')
    return text


def _url_at(text, i):
    """Search "text" for URLs.  Pattern searched for must be
    in the form [some text](a url).

    For example, if text =
    blah blah blah [connect to google](https://www.google.com/) blah
    blah [find a bible verse](https://www.biblegateway.com/)
    blah blah blah [youtube](https://www.youtube.com/)

    and i=2, then https://www.biblegateway.com/w.biblegateway.com/
    is returned.  And if i=3, then https://www.youtube.com/ is
    returned, and so forth"""

    tuples = re.findall(r'(\[.+?\])(\s*\(.+?\))', text)
    if 0 < i <= len(tuples):
        try:
            return tuples[i-1][1][1:-1]
        except Exception as e:
            msg = ('Error at function named _url_i:\n    '
                   + str(e))
            print(msg)
            return None
    else:
        print('Error at function named _url_at.')
        print("    list index out of range")
        return None


class HistoryConsole(code.InteractiveConsole):
    """ This class copied from "https://docs.python.org/3/library/readline.html.
    This class extends the code.InteractiveConsole class to support history
    save/restore.
    """
    def __init__(self, locals=None, filename="<console>",
                 histfile=os.path.expanduser("~/.console-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history(histfile)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.set_history_length(1000)
        readline.write_history_file(histfile)


_read_settingsfn()


if __name__=='__main__':
    try:
        __IPYTHON__
        _in_ipython_session = True
    except NameError:
        _in_ipython_session = False

    if _in_ipython_session:
        print(chr(128073) + ' For ipython do either "ipython -i flashcardz" or "from flashcardz import *"\n')

    if not sys.flags.interactive and not _in_ipython_session :
        vi = sys.version_info
        banner = (f"\nflashcardz running on python {vi[0]}.{vi[1]}.{vi[2]}.  Ctrl+D or quit() closes program.\n" +
                  'How-to instructions are at https://github.com/kcarlton55/flashcardz.\n' +
                  'Excecute "functions()" (w/o quotes) for info about running this program.\n')
        variables = {**globals(), **locals()}
        #shell = code.InteractiveConsole(variables)
        shell = HistoryConsole(variables)
        shell.interact(banner=banner)







