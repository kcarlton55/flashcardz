#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed July 13, 2024

@author: Ken Carlton, kencarlton55@gmail.com

A simple flashcards program used to, among other things, learn another
language.  Flash cards are saved in a local file.  The file has the form:

word1 | definition1 | tally1
word2 | definition2 | tally2
           ...
wordN | definitionN | tallyN

Tally is the number of times the user correctly knew the definition of a word
without a miss. Tally is reset to zero (the default) anytime the user did not
rememember the definition.

Once the maximum tally value has been reached (default is 10), the word is
removed from the card set.  To run the program, run the go() function.
The go() function shuffles the cards before presenting cards to the user.

This program is meant to be run using python's interactive command-line
terminal (i.e. read-eval-print loop (REPL) terminal).  This comes standard when
python is installed on your PC.
"""

#import pdb  # use with pdb.set_trace()
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


__version__ = '0.2.0'   # PEP 440 - describes versions
delimiter = '|'      # pipe symbol
substitute = ';'     # if when file saved, save any pipe symbols as semicolons
default_settings_ = {"maxtally": 10, "tallypenalty": 10, "show_intro": True,
                    "replace_tabs": -1, "abort": False}

def version():
    print(__version__)


def _remains_at_(setting):
    """
    This is subfunction called by _setpathname_(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    try:
        s = _settings_[setting]
        print('\nProgram setting remains at:')
        print(f'    _settings_["{setting}"] = {s}')
    except:
        pass


def _changed_to_(setting):
    """
    This is subfunction called by _setpathname_(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    s = _settings_[setting]
    print('\nProgram setting changed to:')
    print(f'    _settings_["{setting}"] = {s}')
    _write_settings_fn_()


def _currently_at_(setting):
    """
    This is subfunction called by _setpathname_(), etc.

    Parameters
    ----------
    setting : str
        Name of the setting to report info on
    """
    try:
        s = _settings_[setting]
        print('\nSetting is currently:')
        print(f'    _settings_["{setting}"] =  {s}')
    except:
        pass


def _setabort_():
    """
    Change the setting named "abort" to True or False.  If set to True then
    any results, such as tallys, will NOT be recorded when go() is run.
    If False, then results will be recorded.
    """
    global _settings_
    print(_setabort_.__doc__)
    _currently_at_('abort')
    abort = input('\n    abort (Enter nothing for no change) = ').strip()
    if abort == "1" or abort == 'True':
        abort = True
    elif abort == "0" or abort == 'False':
        abort = False
    else:
        abort = None
    if _settings_['abort'] == abort:
        _remains_at_('abort')
    elif abort == False or abort == True:
        _settings_['abort'] = abort
        _changed_to_('abort')
    else:
        print('\nTrue or False are the only valid responses')
        _remains_at_('abort')


def _setshow_intro_():
    """
    Change the setting named "show_intro" to True or False.  If set to True,
    then flashcardz will introduce itself when the flashcardz program starts."""
    global _settings_
    print(_setshow_intro_.__doc__)
    _currently_at_('show_intro')
    show_intro = input('\n    show_intro (Enter nothing for no change) = ').strip()
    if show_intro == "1" or show_intro == 'True':
        show_intro = True
    elif show_intro == "0" or show_intro == 'False':
        show_intro = False
    else:
        show_intro = None
    if 'show_intro' in _settings_ and _settings_['show_intro'] == show_intro:
        _remains_at_('show_intro')
    elif show_intro == False or show_intro == True:
        _settings_['show_intro'] = show_intro
        _changed_to_('show_intro')
    else:
        print('\nTrue or False are the only valid responses')
        _remains_at_('show_intro')


def _settallypenalty_():
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
    global _settings_
    print(_settallypenalty_.__doc__)
    _currently_at_('tallypenalty')
    tallypenalty = input('\n    tallypenalty (Enter nothing for no change) = ')
    if tallypenalty.strip():
        tallypenalty = int(tallypenalty)
    if (isinstance(tallypenalty, int) and ('tallypenalty' not in _settings_)
                                           or tallypenalty != int(_settings_['tallypenalty'])):
        _settings_['tallypenalty'] = abs(tallypenalty)
        _changed_to_('tallypenalty')
    else:
        _remains_at_('tallypenalty')


def _setmaxtally_():
    '''
    Each time the user knows correctly the definition of a word, the tally
    for that word is incremented by one.  When the tally reaches the value of
    "maxtally", the card is removed from the deck.
    '''
    global _settings_
    print(_setmaxtally_.__doc__)
    _currently_at_('maxtally')
    maxtally = input('\n    maxtally (Enter nothing for no change) = ')
    if maxtally.strip():
        maxtally = abs(int(maxtally))
    if (isinstance(maxtally, int) and ('maxtally' not in _settings_
                                       or maxtally != int(_settings_['maxtally'] ))):
        _settings_['maxtally'] = maxtally
        _changed_to_('maxtally')
    else:
        _remains_at_('maxtally')


def _setreplace_tabs_():
    '''
    Replace each tab character with one or more space characters.  To set this
    setting, enter an integer, e.g. 0, 1, 2, 3, etc..  With this set, 0, 1, 2,
    3, etc. spaces will replace each tab character depending in the integer
    that you entered.  This setting only effects the add() function and only
    is activated when the final parenthesis is applied to the add funciton and
    and the Enter key has been pushed.

    To make this setting inactive, set to -1.
    '''
    global _settings_
    print(_setreplace_tabs_.__doc__)
    _currently_at_('replace_tabs')
    replace_tabs = input('\n    replace_tabs (Enter nothing for no change) = ')
    if replace_tabs.strip().isnumeric() or replace_tabs.strip()[1:].isnumeric():
        replace_tabs = int(replace_tabs)
    if (isinstance(replace_tabs, int)
        and ('replace_tabs' not in _settings_
             or replace_tabs != int(_settings_['replace_tabs']))):
        _settings_['replace_tabs'] = replace_tabs
        _changed_to_('replace_tabs')
    else:
         _remains_at_('replace_tabs')


def _setpathname_():
    '''
    Set the pathname (filename prepended by a path) for where your set of cards is
    located.  If the file doesn't exist at the location you specify, it will be created.
    '''
    global _settings_
    print(_setpathname_.__doc__)
    print(f'(current working directory is: {Path().cwd()})')
    _currently_at_('pathname')
    print("\nEnter pathname for new or existing file (e.g. C:\\mypath\\myfile.txt)")
    userinput = input(r'    Pathname (Enter nothing for no change) = ').strip()
    fn = Path(userinput)
    fn_resolved = fn.resolve()
    current_fn = Path(_settings_['pathname']).resolve()
    if userinput and  fn_resolved.is_dir():
        print(f'\npathname cannot be a directory. You tried to create {fn_resolved}')
        _remains_at_('pathname')
    elif userinput and not fn_resolved.parent.exists():
        print(f'\nParent directory {fn_resolved.parent} does not exist.')
        print('Withont a parent directory your file cannont be created.')
        _remains_at_('pathname')
    elif  userinput and fn_resolved == current_fn:
        print("You didn't change the pathname.")
        _remains_at_('pathname')
    elif userinput and fn_resolved.exists():
        print('\nFile already exists.  Will use that file.')
        _settings_['pathname'] = str(fn_resolved)
        _changed_to_('pathname')
    elif (userinput and not fn_resolved.exists()) or (userinput and fn_resolved.exists()):
        _settings_['pathname'] = str(fn_resolved)
        _changed_to_('pathname')
    else:
        _remains_at_('pathname')


def settings():
    """Adjust program's settings to tailer the behavior to fit your needs.

    Example
    -------
    >>> settings()
    """
    global _settings_
    flag = False
    for key, value in default_settings_.items():
        if key not in _settings_:
            _settings_[key] = value
            flag = True
    if flag:
        _write_settings_fn_
    print(settings.__doc__)
    print(f"Settings are saved in file {_get_settings_fn_()}.")
    print('If this file is erased, once flashcardz is rerun, file will be recreated')
    print('with settings reset to defaults.')
    print('\nCurrent settings are:')
    for key, value in _settings_.items():
        print(f'    {key}: {value}')
    chgkey = input('\nSetting to change (Enter nothing for no change): ')
    print()
    chgkey = str(chgkey).strip().lower()
    if chgkey and chgkey not in _settings_.keys():
        print(f'\n"{chgkey}" not found')
        closest = get_close_matches(chgkey, _settings_.keys(), 1)
        if closest:
            print(f'Perhaps you meant this?: {closest[0]}')
        else:
            print('\nAvailable choices:')
            for k in _settings_.keys():
                print(f'    {k}')
    if chgkey == 'pathname':
        _setpathname_()
    elif chgkey == 'maxtally':
        _setmaxtally_()
    elif chgkey == 'abort':
        _setabort_()
    elif chgkey == 'tallypenalty':
        _settallypenalty_()
    elif chgkey == 'show_intro':
        _setshow_intro_()
    elif chgkey == 'replace_tabs':
        _setreplace_tabs_()


def functions():
    ("Functions are:  add(), cards(), delete(), functions(), go(), settings()\n"
     "and version().\n\n"

     "The primary functions are add(), cards(), and go().\n\n"

     "Enter help(functionname) to learn more about a function.  Enter\n"
     "print(__doc__) to see an overview of this program.\n\n"

     "Examples\n"
     "--------\n\n"

     ">>> help(add)\n\n"

     ">>> help(go)\n\n"

     "\x1b[0;1;31mNOTE: Push the q key to exit help.\x1b[0m")
    print(f'\n{functions.__doc__}')


def add(word, definition, tally=None):
    """ Add a new card to your card deck.  (This function will automatically
    open the file that contains your deck of cards, add your new card, and then
    save the updated data to your file.)

    Parameters
    ----------
    word : string
        New word to add to the deck of cards.  (A string, by the way, in python
        is text surrounded by quotation marks, e.g. 'house (noun)'; though
        triple quotes works and at times aids in the task of adding and editing
        cards. i.e. '''house (noun)''').

        If a word is found to already exist (exact same letters) then the
        definition of that word is replaced by the new definition that you
        enter.

    definition : string
        Definition of the word.  Surround your string with quotation marks.  If
        your string is multiline, surround your string with triple quotes, e.g.:
        ''' a building that serves as living quarters for one or a few
        families; a shelter, refuge.'''

        URL links can be included within a description.  URL links must have
        the form [some text](a url).  For example, a description which includes
        a URL link will look like: '''blah blah blah
        [connect to google](https://www.google.com/) blah blah'''.  See
        help(go) and help(cards) to see how a user is to activate these links.

        You can have portions of your text highlighted with italics,
        underlined, or have a different color text such as red or green.  To
        learn how to do this, read the doumentation at an internal function
        that flashcardz utilizes by entering: help(_modify_text_)

    tally : int
        Set the tally to a value you choose. Normally let the program set
        this value for you.  Tally is automaticaly set to 0 when you enter a
        new word and definition.  If the word you enter already exists, then
        tally is set to value of that word.  However you can override any of
        these automatic settings by entering a value that you deem suitable.

    Examples
    --------

    >>> add('taza nf', '(bol con asa)  cup n, mug n')


    #  When go() is run, word and desription will show as:
    #
    #    taza nf
    #
    #    (bol con asa)  cup n, mug n


    >>> add('''correr vi''',
        '''(moverse deprisa)
           run vi
           (rush) get a move on v expr
           go quickly, go fast vi + adv''')


    #  When go() is run, word and desription will show as:
    #
    #    correr vi
    #
    #    (moverse deprisa)
    #         run vi
    #         (rush) get a move on v expr
    #         go quickly, go fast vi + adv


    >>> w = 'correr vi'

    >>> d = '''(moverse deprisa)
            run vi
            (rush) get a move on v expr
            go quickly, go fast vi + adv'''

    >>> print(d)   # Not necessary to use, but helpfull.  Shows a preview of output.

    >>> add(w, d)


    #  Using w and d as shown above is another way to achieve the same result.
    #
    #  Tip 1: If the definition you entered isn't to your satifaction, push the
    #  up key so that the add function you previously entered reappears, then
    #  edit the definition. (Word cannot change, otherwise deck will be added
    #  to instead of a card revised.)
    #
    #  Tip 2: When pasting a word AND its defintion, is is recommended to start
    #  with add(''' and then paste text that you copied from some source.  To
    #  move the cursor within your pasted text in order to edit it, use the key
    #  board's arrow keys.
    """
    if word and definition and type(word) == str and type(definition) == str:
        _cards_ = _open_()
        word = word.replace(delimiter, substitute).strip()
        definition = definition.replace(delimiter, substitute).strip()
        if 'replace_tabs' in _settings_ and _settings_['replace_tabs']:
            i = _settings_['replace_tabs']
            word = word.replace('\t', i*' ')
            definition = definition.replace('\t', i*' ')
        word0 = ''.join(word.split()).lower()  # white space removed
        for i, x in enumerate(_cards_):
            x0 = ''.join(x[0].split()).lower()
            if x0 == word0:  # if word already in _cards_, delete it to replace with new
                _cards_.pop(i)
                t = tally if tally and isinstance(tally, int) else x[2]

                _cards_.insert(i, [word, definition, t])
                break
        else:
            t = tally if tally and isinstance(tally, int) else 0
            _cards_.append([word, definition, t])
        print(f'\n{_modify_text_(word)}\n\n{_modify_text_(definition)}\n')
        print('Number of cards now at: ', len(_cards_))
        print()
        _save_(_cards_)
    else:
        print('\nError at add function.  Here is an example of how to do it:\n')
        print('add("pill", "a small round mass of solid medicine to be swallowed whole.")')


def delete(number=None):
    '''
    Delete a card from the deck.  Use cards() to see the row numbers that
    correspond to the card in your deck.

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
    _cards_ = _open_()
    if not number == None:
        number = abs(int(float(number)))
    if number == None:
        print('Card number to delete?  (Run function cards()')
        print('to see what word corresponds to what number.)\n')
        number = input('Number: ')
    if isinstance(number, str):
        number = abs(int(float(number)))
    if number < len(_cards_):
        print(f'\nCard {number} is: {_cards_[number][0]}.\n')
        confirm = input(f'Delete card {number}? [Y/n): ')
        if confirm.lower() not in ['n', 'no']:
            print(f'\nCard {number} deleted ({_cards_[number][0]})\n')
            _cards_.pop(number)
            print('Number of cards now at: ', len(_cards_))
            _save_(_cards_)
        else:
            print(f'Card {number} not deleted.')
    else:
        print(f"Card number {number} doesn't exist.")


def _save_(_cards_):
    '''
    Save your cards to a file.  File format is text, meaning that it can be
    opened with a text editor.  Furthermore, the file is structured in csv
    format, meaning that it can opened with Microsoft Excel.  Note that if you
    open the file with Excel, Excel may ask what delimiter the csv file uses.
    The delimiter you should use is the vertical bar character, |.

    Since the delimiter is a |, i.e. the character used separate column
    fields, | characters are not allowed in text that you enter for a word or
    its definition.

    Parameters
    ----------
    _cards_ : list
        list of cards that has the format:
        cards = [['word1', 'definition1', 'tally'],
                 ['word2', 'definition2', 'tally'],
                   ...,
                 ['wordN', 'definitionN', 'tally']]

    Elements of the list are strings execept for 'tally' which are integers.

    '''
    if ('pathname' not in _settings_ or _settings_['pathname'] == None
            or _settings_['pathname'] == ""):
        _setpathname_()
    fields = ['word', 'definition', 'tally']
    try:
        fn = Path(_settings_['pathname'])
        with open(fn, 'w', newline='', encoding='utf-8', errors='replace') as csvfile:  # w/o newline='', blank lines inserted with MS Windows
            csvwriter = csv.writer(csvfile, delimiter=delimiter)
            csvwriter.writerow(fields)
            csvwriter.writerows(_cards_)
    except Exception as e:
        msg = ("Error at _save_ function:\n\n"
               "Unable to save flashcardz data file.\n"
               "Perhaps you have it open with another program?\n  "
               + str(e))
        print(msg)


def _open_():
    '''
    Open the pathname specified in flashcardz' _settings_, then read its
    contents.  Convert those contents to a python list object.  The file that
    is opened is specfied in flashcardz' _settings_ at '_settings_["pathname"]'

    Returns
    -------
    _cards_ : list
        List of words and their difinitions; included is the tally for that
        word. (tally: number of times a user has correctly known the defintion
        of a word.)

    '''
    try:
        if ('pathname' not in _settings_ or _settings_['pathname'] == None
                or _settings_['pathname'] == ""):
            _setpathname_()

        fn = Path(_settings_['pathname'])

        _cards_ = []
        with open(fn, 'r', encoding='utf-8', errors='replace') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter)
            for _card in csvreader:
                ln = len(_card)
                if 1 < ln < 3:
                    del _card[2:]
                    _card.append('0')
                elif ln == 1:
                    print('\nSomething is wrong with your data file.  At least one line in the file contains\n'
                           'data that would fill only one field, and not multiple fields, i.e. the word and\n'
                           'description fields.  The most likely reason for this is that the file was not\n'
                           'saved in a csv file format suitable for the flachcardz program.   The file\n'
                           'should be a csv file that uses a pipe/vertical bar character, |, as a delimiter.')
                    sys.exit()
                if not _card[2].isnumeric():
                    _card[2] = '0'
                if not _card[0] == 'word':
                    _cards_.append(_card)
    except Exception as e:
        msg = ('Error within function named "_open_ function".\n'
               + str(e))
        print(msg)
    return _cards_


def cards(cmd=True, i=None):
    """From the cards' data file, show a list of all words with, or without,
    their defintions.

    Parameters
    ----------
    cmd (optional) : bool | int | tuple
        if cmd == True or is no value is given (i.e. cards()), then show a
            list of all words but without definitions.
        if cmd == False; show all words AND their definitions.
        if type(cmd) == int (i.e. integer); at position "int" show word and its
            definition. (do "cards()" to see integers that correspond to words)
        if type(cmd) == tuple, and the tuple contains two intergers, show a
            list of cards starting at the first number and ending at the
            second.  A tuple is a set of values surrounded by parentheses,
            e.g., (5, 20)

    i : int
        URL links (see add() function) can exists in the description field of
        for a given word.  If so, then i represents the 1st, 2nd, etc. link.
        Entering that number will cause a web browser to open that link.
        If i is a negative number, show links as well as the coding that shows
        text italized, underlined, and/or colored  Note: this only works if
        "cmd" is an int not a tuple or boolean.

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

    # Same as above, but remove any invisible, lurking tab characters:
    >>> cards('8')

    # Open a web browser and with it open the 2nd link shown in the
    # description for card 8.  (Links will be seen surrounded by brackets, []).
    >>> cards(8, 2)

    # Show card 8, but this time show the url, e.g. https://www.python.org/,
    # and also show any code that the user entered to italicize, underline, or
    # color an portions of text.
    >>> cards(-8)    # i.e., enter card 8 as a negative number.

    # Show to the user a list cards, 5 to 9:
    >>> cards((5, 9))

    # Tip: Create a shortcut for youself by making a copy of the cards function:
    >>> c = cards
    >>> c(8)

    """
    _cards_ = _open_()
    separator = 35*'-'
    if type(cmd) == int and cmd >=0 and i == None:  # Show one word and its decrip
        j = cmd
        _card = _cards_[j]
        word = _modify_text_(_card[0])
        desc = _hide_urls_(_card[1])
        desc = _modify_text_(desc)
        k = "'''" if  '\n' in word else "'"
        print(f"\n{k}{word}{k},\n'''\n{desc}\n'''")
    elif type(cmd) == int and cmd < 0 and i == None:  # w/ urls & color codes
        print('aaa')
        print(type(cmd))
        j = abs(cmd)
        _card = _cards_[j]
        word = _card[0]
        desc = _card[1]
        k = "'''" if  '\n' in word else "'"
        print(f"\n{k}{word}{k},\n'''\n{desc}\n'''")
    elif type(cmd) == float and (-.9999 <= cmd < 0) and i == None:  # w/ urls & color codes
        j = 0
        _card = _cards_[j]
        word = _card[0]
        desc = _card[1]
        k = "'''" if  '\n' in word else "'"
        print(f"\n{k}{word}{k},\n'''\n{desc}\n'''")
    elif isinstance(cmd, str) and cmd.isnumeric() and i == None:
        j = int(cmd)
        _card = _cards_[j]
        word = _modify_text_(_card[0]).replace('\t', ' ')
        desc = _hide_urls_(_card[1])
        desc = _modify_text_(desc).replace('\t', ' ')
        k = "'''" if  '\n' in word else "'"
        print(f"\n{k}{word}{k},\n'''\n{desc}\n'''")
    elif isinstance(cmd, str) and cmd[1] == '-' and cmd[1:].isnumeric() and i == None:
        j = abs(int(cmd))
        _card = _cards_[j]
        word = _card[0].replace('\t', ' ')
        desc = _card[1].replace('\t', ' ')
        k = "'''" if  '\n' in word else "'"
        print(f"\n{k}{word}{k},\n'''\n{desc}\n'''")
    elif type(cmd) == int and isinstance(i, int):  # open url at position i
        j = abs(cmd)
        _card = _cards_[j]
        webbrowser.open(_url_at_(_card[1], i))
    elif type(cmd) == tuple and len(cmd) ==  2:
        a = min(cmd)
        b = max(cmd) + 1 if max(cmd) < len(_cards_) else len(_cards_)
        for j in range(a, b):
            _card = _cards_[j]
            word = _modify_text_(_card[0])
            desc = _hide_urls_(_card[1])
            desc = _modify_text_(desc)
            text1 = f'{j}. {word : <30} (tally: {_card[2] : >})' # the ": <30" and ">" alligns text
            text2 = (f'{separator} tally: {_card[2]} {separator}\n' +
                     f'{j}. {word}\n' + f'{desc}')
            print(text1)
    else:
        for j, _card in enumerate(_cards_):  # show a list of all cards.  If cmd==False, also show definitions
            word = _modify_text_(_card[0])
            desc = _hide_urls_(_card[1])
            desc = _modify_text_(desc)
            text1 = f'{j}. {word : <30} (tally: {_card[2] : >})' # the ": <30" and ">" alligns text
            text2 = (f'{separator} tally: {_card[2]} {separator}\n' +
                     f'{j}. {word}\n' + f'{desc}')
            print(text1) if (cmd == 1 or cmd == True) else print(text2)


def go(shuffle=True):
    '''
    First the deck of cards in shuffled.  Then one by one each card is shown
    to the user.  First the word is shown.  The user looks at the word and
    tries to figure out the meaning of the word.  Then the user hits any key.
    The defintion is then shown.  The user is asked if he/she knew what the
    word means.  If he/she answers yes, then the tally is incremented by one.
    (Tally is the number of times the user knew what the word means.)  If the
    user didn't know, the the tally for that word is reset to zero (or another
    value defined by the setting that the user set).

    Once a max tally is reached (determined by the user's settings), the
    card is removed from the deck.

    When go() is run, the file that contains the card deck is opened.  After
    all the cards are viewed by the user, the updated card deck is saved.  If
    the user aborts viewing the cards before go() is finished, results are not
    saved.

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
    print("         the 1st, 2nd, 3rd, etc. url link within a description (that is, if the")
    print("         link exists).  Links are enclosed in brackets, [].")
    if _settings_['abort'] == True:
        abort = True
        print('     (Note: _settings_["abort"] = True.  RESULTS WILL NOT BE SAVED!)')
    else:
        print("     a = abort recording of results when go() completes its run")
    print("     q = cancel showing cards")
    print("    " + 75*"—")

    print()
    ans1 = input("Press Enter to start. ")
    if ans1 and (ans1[0].lower() == 'q' or ans1[0].lower() == 'e'):
        return

    print("\nHere we go!")

    _cards_ = _open_()
    index_list = [i for i in range(0, len(_cards_))]
    if shuffle == True and len(_cards_) > 2:
        print("\nShuffling cards ", end='')
        for i in range(15):
            print(">", end='')
            time.sleep(.08)
        print()
        index_list = sorted(index_list, key=lambda x: random.random())

    number = 0
    number_of_cards_ = len(_cards_)
    abort = False
    unwanted = []
    missed = []
    print()
    correcttext = ('Meaning known? (Y/n/i/q) ' if _settings_['abort']
                   else 'Meaning known? (Y/n/i/a/q) ')

    for k in index_list:
        number += 1
        loop = True
        flag = True
        while loop:
            print(35*'-' + ' tally: ' + str(_cards_[k][2]) + ' ' + 35*'-')
            print(f'{number} of {number_of_cards_}.  {_modify_text_(_cards_[k][0])}')  # _cards_[k][0] is "word"
            if flag:  # pause after word shown, but pause only once.
                flag = False
                ans0 = input()
                if ans0 and (ans0[0].lower() == 'q' or ans0[0].lower() == 'e'):
                    return
            desc = _hide_urls_(_cards_[k][1])  # _cards_[k][1] is "description"
            desc = _modify_text_(desc)
            print(f'{desc}\n')
            ans = input(correcttext)

            if ans and ans.isnumeric():
                webbrowser.open(_url_at_(_cards_[k][1], int(ans)))
            elif ans and ans[0].lower() == 'i':
                print('\n    Entering "i" is inappropriate.  Instead enter 1, 2, 3, etc., depending on')
                print('    which URL link is shown in brackets, [], that you wish to activate; i.e. the')
                print('    1st, 2nd, 3rd.\n')
            elif ans and (ans[0].lower() == 'q' or ans[0].lower() == 'e'):
                return
            elif ans and ans[0].lower() == 'a' and abort == False:
                abort = True
                correcttext = 'Correctly answered? (Y/n/i/q) '
                print("    " + 75*"—")
                print('     Results will NOT be recorded when go() completes its run')
                print("    " + 75*"—")
                # loop = True is the default, so user will be asked again... Y/n/i/a/q
            elif ans and ans[0].lower() == 'a' and abort == True:
                abort = False
                correcttext = 'Correctly answered? (Y/n/i/a/q) '
                print("    " + 75*"—")
                print('     Results WILL be recorded when go() completes its run')
                print("    " + 75*"—")
            elif ans and ans[0].lower() == 'n':
                print()
                _cards_[k][2] = max(0,  _settings_['maxtally'] - _settings_['tallypenalty'])
                missed.append(_cards_[k])
                loop = False
            elif ans and ans[0].lower() == 'y':
                print()
                _cards_[k][2] = int(_cards_[k][2]) + 1    # _cards_[k][2] is "tally"
                if _cards_[k][2] >= _settings_['maxtally']:
                    unwanted.append(k)
                loop = False
            else:
                print()
                _cards_[k][2] = int(_cards_[k][2]) + 1
                if _cards_[k][2] >= _settings_['maxtally']:
                    unwanted.append(k)
                loop = False
    print(32*" " + "=== The End ===")

    if unwanted:
        unwanted = sorted(unwanted)
        print('\n' + 80*'_')
        if not abort:
            print(
                'Congradulations!  Max tally reached on the following.  Cards removed: \n')
        else:
            print('Congradulations!  Max tally reached on the following: \n')
        # [::-1] reverses the list in order to remove latter elements first.
        for ele in unwanted[::-1]:
            # ele is an element of the _cards_ list
            print(f'    {_cards_[ele][0]}')
            del _cards_[ele]
        print()
        if not abort:
            print(f'\nNumber of cards is now {len(_cards_)}\n')

    if missed:
        print('\n' + 80*'_')
        percent = str(int(100*(len(_cards_) - len(missed))/len(_cards_)))
        print(f'{percent}% answered correctly!')
        print('These are the words you missed: \n')
        im0 = []
        for m in missed:
            i = _cards_.index(m)
            im0.append([i, m[0]])
        im0.sort(key=lambda x: x[0])
        for k in im0:
            print(f'{k[1]}') if abort and unwanted else print(f'{k[0]}. {k[1]}')
        print()
    else:
        print('\n' + 80*'_')
        if len(_cards_) == 0:
            print('Card deck is empty.  Please add data.')
        else:
            print('100% of list answered correctly!')
    if not abort:
        _save_(_cards_)


def _get_settings_fn_():
    '''Get the pathname (path and name) to store user's settings.  The file
    will be named _settings_.txt.  The pathname will be vary depending on who's
    logged in and what os is being used.  Pathname will look like:
    C:\\Users\\Ken\\AppData\\Local\\flashcardz\\_settings_.txt.  On a linux
    os, will look like: /home/Ken/.flashcardz/_settings_.txt

    If the pathname does not already exists, it will be created, and default
    settings will be inserted into the file, i.e.
    {"maxtally": "10", "abort": "False", etc. }
    '''
    if sys.platform[:3] == 'win':  # if a Window operating system being used.
        datadir = os.getenv('LOCALAPPDATA')
        path = os.path.join(datadir, 'flashcardz')
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        settingsfn = os.path.join(datadir, 'flashcardz', '_settings_.txt')

    elif sys.platform[:3] == 'lin':  # if a Linux operating system being used.
        homedir = os.path.expanduser('~')
        path = os.path.join(homedir, '.flashcardz')
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        settingsfn = os.path.join(homedir, '.flashcardz', '_settings_.txt')

    else:
        printStr = ('At method "get_configfn", a suitable path was not found to\n'
                    'create file settings.txt.  Notify the programmer of this error.')
        print(printStr)
        return ""

    _bool = os.path.exists(settingsfn)

    # Whoops.  A settingsfn doesn't aready exist.  Create one on user's computer
    if not _bool or (_bool and os.path.getsize(settingsfn) == 0):
        fn_2_suggest = _suggest_fn_()
        print('\n\n It appears this is your first time running this program.  A file\n'
              ' name needs to be established in which a new card deck will be\n'
              ' started.  Please provide a pathname; i.e. filename prepended with a path.')
        print('\n')
        fn = input(fr'    file name ({fn_2_suggest}): ')
        fn = fn.strip()

        if not fn:
            fn = str(fn_2_suggest)
            print('\nProgram setting pathname set to:')
            print(f'    _settings_["[pathname"] = {fn}')
        with open(settingsfn, 'w') as file:         # if a settingsfn doesn't exist, create one with default settings
            _settings_ = default_settings_    # _settings_ here is not global
            _settings_['pathname'] = fn
            file.write(str(_settings_))
    return settingsfn


def _read_settings_fn_():
    global _settings_
    try:
        settingsfn = _get_settings_fn_()
        with open(settingsfn, 'r') as file:
            x = file.read().replace('\\', '/')
        _settings_ = ast.literal_eval(x)
    except Exception:
        msg = ("\n\n\n\x1b[0;1;31mError occured at the _read_settings_fn_() function:\n"
               "It is possible that your settings file is corrupt.  Deleting the\n"
               "file will most likely fix the problem.  (But will reset your settings to\n"
               "defaults.)  File to delete is: \n\n")
        msg += _get_settings_fn_() + "\x1b[0m"
        print(msg)


def _write_settings_fn_():
    '''Write the dictionary named _settings_ to to a file.  _settings_ contains
    user user modified settings via the settings() function.

    Returns
    -------
    None.

    '''
    try:
        settingsfn = _get_settings_fn_()
        with open(settingsfn, 'w') as file:
            file.write(str(_settings_))
    except Exception as e:
        msg = ("\nError at _write_settings_fn_() function:\n\n"
               "Unable to save flashcardz data file.\n"
               "Perhaps you have it open with another program?\n  "
               + str(e))
        print(msg)


def _suggest_fn_():
    '''
    Suggest a file name to the user.

    Returns
    -------
    str
        pathname

    '''
    home_dir = Path.home()
    doc_dir = Path.home().joinpath('Documents')
    if doc_dir.is_dir():
        return doc_dir / 'flashcardz.txt'
    elif home_dir.is_dir():
        return home_dir / 'flashcardz.txt'
    else:
        pass


def _hide_urls_(text):
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


def _url_at_(text, i):
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
        print('Error at function named _url_at_.')
        print("    list index out of range")
        return None


def _modify_text_(text):
    """This is an internal function of flashcardz.  It facilitates the user to
    insert ansi escape codes into his text.  This then allows the user to show
    selected text underlined, italicized, and/or colored.  For example, if a
    word description is "my long, lengthy description", and the user adds
    special coding within it like "my long, <g>lengthy<> description", then the
    text "lengthy" will be shown with green letters to the user.

    The keys that may be used to alter text are:
    k=black, r=red, g=green, y=yellow, b=blue, p=purple, c=cyan, w=white
    i=italics, 1=bold, u=underline, x=cross out.

    Making text bold (code "1") makes colors brighter.

    Background colors to text can also be added.  Background color keys are:
    K=black, R=red, G=green, Y=yellow, B=blue, P=purple, C=cyan, W=white

    More than one code can be entered at a time, for example
    "my long, <g1ui>lengthy<> description" will make "lengthy" bright green,
    underlined, and with italicized text.

    As you will have already noticed, the syntax is:
    <code letters>text to modify<>

    Note:  Altering text as described above may not work on your system.  It
    depends on whether your operating system, the version of your operating
    system, and/or whether your console supports it or not.

    Parameters
    ----------
    text : string
        The text to alter.  The text can include the codes that are to alter
        the text.

    Returns
    -------
    text : string
        Returns the same text that was input to the function, but ansi escape
        codes will replace the user supplied codes.  Witn ansi escape codes,
        text will look like \x1b[0;3;1m\\x1b[0;32mtext to modify\\x1b[0m\x1b[0m.  (The user will
        never see this code.)  In this example, the text will be shown green.
        If the user entered no code, then the text remains unchanged.

    Examples
    --------
    >>> _modify_text_('''(moverse deprisa)
                         run vi
                         (rush) get a move on v expr
                         <ur1>go quickly<>, go fast vi + adv''')

    # An example of how the user will make use of this function when using the
    # flashcardz program:
    >>> add('''correr vi''',
        '''(moverse deprisa)
           run vi
           (rush) get a move on v expr
           <ur1>go quickly<>, go fast vi + adv''')

    """
    colors = {'k':'30', 'r':'31', 'g':'32', 'y':'33', 'b':'34',
              'p':'35', 'c':'36', 'w':'37'}
    mods = {'i':'3', '1':'1', 'u':'4', '0':'22', 'x': '9'}
    backgrounds = {'K':'40','R':'41', 'G':'42', 'Y':'43', 'B':'44',
                   'P':'45', 'C':'46', 'W':'47'}
    dics = {**colors, **mods, **backgrounds}
    pattern = r'<(\w+)>(.+?)<>'
    lst = re.findall(pattern, text)
    for l in lst:
        code = ['\x1b[', '0;']
        for x in l[0]:
            if x in dics:
                code.append(dics[x])
                code.append(';')
        code.pop()
        code.append('m')
        code = ''.join(code)
        old_value = f'<{l[0]}>{l[1]}<>'
        new_value = (code + l[1] + '\x1b[0m')
        text = text.replace(old_value, new_value)
    return text


_read_settings_fn_()

vi = sys.version_info
banner = (f"\nflashcardz {__version__} running on python {vi[0]}.{vi[1]}.{vi[2]}.  Ctrl+D or quit() closes program.\n" +
          'How-to instructions are at https://github.com/kcarlton55/flashcardz.\n' +
          'Excecute "functions()" (w/o quotes) for info about running this program.\n')
try:
    if _settings_['show_intro']:
        print(banner)
except:
    print(banner)


if __name__=='__main__':
    pass









