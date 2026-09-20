# **flashcardz**

## **Intro**

flashcardz is learning aid to learn foreign languages.  A word is shown on the screen, then followed by the word's definition.  A score is tallied whether you knew the word or not.  After multiple viewings of cards, once a card's maximum tally is reached, the card is removed.

## **Install Python**

flashcardz runs via the Python interpreter.  The Python interpreter is free.  It can be downloaded from www.python.org

## **Install flashcardz**

Once Python is installed, using a [command window](https://www.igmguru.com/blog/what-is-command-prompt) use the "pip" command that comes with Python.  It will download and install flashcardz onto your computer. Enter this into the command window: 

`C:\> pip install flashcardz`

This downloads and installs flashcardz from a repository site named pypi.org

## **Start up flashcardz**

From a [command window](https://www.igmguru.com/blog/what-is-command-prompt) do:

`C:\> py`

This opens the Python interpreter, also called a [Python REPL](https://www.youtube.com/watch?v=vCYDRcVrnFA).  In the REPL enter:

`>>> from flashcardz import *` 

This loads flashcardz into the current REPL session.

## **Quick start**
#### add()

Use the *add* function to add new words:
```
>>> add('correr vi', 
'''
(moverse deprisa)     run vi
            (rush)    get a move on v expr
                      go quickly, go fast vi + adv''')
			
			
>>> add('mesa nf',
'''
(mueble con patas)   table n
    (furniture with flat top)''')
```			  
As seen, the format of *add* is:

`>>> add('new word','''definition of the new word''')`

The triple quotes, ''', are used to surround text that spans multiple lines.

#### cards()

To view the words you now have in the card stack, enter:

`>>> cards()`

If you have say 20 words in your card stack, and you want to see the words and definitions for a subset of those cards, do:

`>>> cards(8, 15)`

This will show cards starting at card 8 and ending at the card just before card 15; i.e. card 14.

#### go()

Now to suffle the stack and test your memory about word definitions do:

`>>> go()`

## **Upgrade**

To get the latest version of flashcardz installed onto your computer, do:

`pip install --upgrade flashcardz`

## **Import/Export to Excel**

When you execute flashcardz' `settings()` function, you will see the location of the file where flashcardz' word/definition data is stored. You can import/export that data to Excel.  The instructions here will not show you how to do this, but will rather point you in the direction to where you can figure out how to do this for yourself.  The main thing to know is that flashcardz' data is in csv format and uses the pipe character, |, as a delimeter.

Here is a link to one how-to: [Import/Export csv files to Excel]( https://websitebuildersupport.web.com/article/1683-import-export-csv-files-to-excel)

If you do an Internet search, you'll find other similar tutorials.
