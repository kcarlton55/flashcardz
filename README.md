# **flashcardz**

## **What the program does**
Flashcardz is used to aid in the learning a foreign language, math tables, etc.
One-by-one a word, then its defintion, is shown to the user.  A card's tally is
incremented each time the user correctly recalled a word's defintion.  Cards
are removed once a card's maximum tally has been reached.

The program runs from python's command line terminal, i.e its [REPL](https://www.pythonmorsels.com/using-the-python-repl/).  Use
flashcardz go() function to show cards one-by-one:

`>>> go()`

Adding words words to your deck of cards is easy.  Use flashcardz's add()
function:

`>>> add('correr', 'to run (to move quickly on two feet)')`

Words and definitions can also be imported from an Excel file.


## **Features**
* Cost: Free.
* Easily add words and defintions via copy and paste.
* User can imbed url links into cards.
* Can import words and definitions from an Excel file.
* Deck is shuffled before each viewing.
* Score (i.e. a tally) is kept for each time word is successfully known.
* Cards whose max tally has been reached are removed from the deck.
* A card automatically removed each time its max tally has been reached.
* Portions of card's text can be highlighted with underscores, italics, or colors.
* Issue a trigger to a card, i.e. a key; Opens an web page from the Internet
  showing the word's definition.
* Run Flashcardz from a web page when Jupyter Lab software is installed.


## **How to install**
For this program to run, it requires both python (which is free) and
flashcardz.py to be installed on your computer.

To install python, download and install it from, [python.org](https://www.python.org/).

To install flashcardz.py, open a Window's command prompt
(References: (1. [how to open a command prompt](https://www.youtube.com/watch?v=uE9WgNr3OjM), 2. [command prompt basics](https://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/))
and enter into the command prompt:

`C:\> pip install flashcardz`

(C:\>  is the command prompt.  Don't enter that.)  Pip is a program that gets
automatically installed when python is installed.  Pip fetches python programs
from [pypi.org](https://pypi.org/) and installs them on your computer.  (For
more info about pip, see [How to use pip](https://note.nkmk.me/en/python-pip-usage/)).

Here is how you can update flashcardz to its latest version or uninstall it:
```
C:\> pip upgrade flashcardz

C:\> pip uninstall flashcardz
```

## **How to run flashcardz**

Open a command prompt and start up a python session.  In MS Windows, this is
usually done by entering *py*.  On other operating systems, *python*:

```
C:\> py
Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

As shown above, some introductory info is shown.  You can ignore it.  At the
command prompt, i.e. the chevron (>>>), load flashcardz like this:

`>>> from flashcardz import *`

This imports flashcardz' functions with which you can control flashcardz.

>Another way you can start flashcardz is if you downloaded flashcardz.py
>directly from its home site at https://github.com/kcarlton55/flashcardz.
>Start it up like this:
>
>`C:\> py -i flashcardz.py`
>
>The -i switch causes flashcardz to automatically open in *interactive* mode,
>i.e. opens the python REPL terminal for input and loads in flashcardz' functions.
>(reference: [Open Command Prompt in Current Folder or Directory](https://www.youtube.com/watch?v=bgSSJQolR0E))

To see a list of flashcardz' functions and how do use them do:

`>>> functions()`

To add cards for use by flashcardz, use the add() function:

`>>> add('amigo, amiga nm, nf', '(camarada) friend n buddy n')`

That is, the structure should be add('my word', 'my definition').  Each time
you use the add() function, the data you enter is added to a data file for
later use.  If you would like to add a multiline definition, do so like this:

```
>>> add('''amigo, amiga nm, nf''',
'''
(camarada) friend n buddy n

Nuestro primer viaje, a Cuzco, lo organizamos entre cuatro amigos.
We organized our first trip, to Cuzco, among four friends.

[how to pronounce](https://www.wordreference.com/es/en/translation.asp?spen=amigo)
''')
```

As you can see, use three quotation marks, ' ' ', to surround text when entering
multiple lines.  Note: you don't have to type all this in manually.  Find a
word's difintion on the Internet, copy words and definitions from there, and
paste them into the REPL.  Notice the last line in the definition.  It is a URL
link.  URL links can be inserted into a word's definition using brackets and
parenthesis using the format `[link description](URL)`

To see a list of your cards, and the number of the card according to its
location in the deck, do:

`>>> cards()`

To see the definition of, for example, card no. 9 in the deck, do:

`>>> cards(9)`

When you're ready to view the cards one-by-one and test you memory of the
words, run the go() function:

`>>> go()`

When the go() function is run, it automatically opens up the data file that
contains your words and definitions, reads the data into memory, closes the file,
and then begins showing the cards.  When the go() function completes its task,
tallies are updated, cards where maximum tallies have been reached are removed
from the deck, the data file is reopened, updated data is saved, and finally
the file is closed.  It typically takes less than a second to open, close, and
move data in and out of the data file.

When you want to exit python, enter either *quit()*, *exit()*, or *Ctrl+D* (or
simply *quit* or *exit* works for python 3.13 and up):

`>>> quit()`

## **Convert an Excel file to a flashcardz data file**

Words and definitions can be created in Excel and then exported to a text file
that flashcardz can open and read.  First, in cells A1 and B1 of the Excel file
enter the column headers.  Use as column headers "word" and "definition"
(without the quotation marks) for these two cells.  In  subsequent rows, 2, 3,
4, etc. put in your words and definitions.

Save your file.  Don't save it to a typical xlsx format.  Save it instead to
a cvs format.  If you are not aware of this file format, please see this
explanation: [Comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values).
Futhermore UTF-8 character encoding is required.  In Excel, when you do a
"Save As", look for "CSV UTF-8 (Comma delimited)(*.csv)".  (However, read on...
a bug exists.)

There is a problem using the normal way that Excel exports to a csv file.  The
csv file that Excel exports to will have columns (i.e. the word and definition
columns) separated by commas.  That's well and good, but many times, like shown
in the "add" example above, when copying and pasting definitions from the
Internet, commas will be included within the definitions.  When flashcardz
reads in the csv file the result will be that flashcardz will interpret the
additional commas to mean that your deck has additional columns, i.e. columns
that shouldn't exist.  This will cause flashcardz to crash.

To remedy this situation, flashcardz was instead coded to recognize the
pipe, i.e. vertical bar character, |, as the separator (more specifically
called a delimiter).  Excel was somewhat poorly designed because Excel does not
allow to change to a different delimiter when exporting.  But there is a
relatively easy work-around.  See this youtube video for how to do it:
[Export Data with Pipe Delimiters Instead of Commas](https://www.youtube.com/watch?v=jieWzHJjVBU)


## **Opening a flashcardz data file into Excel**

Opening a flashcardz data file into Excel is relatively easy.  When you open a
flashcardz data file (with a csv or txt extension), you will be given the
option to use a different delimiter other than a comma.  Use the vertical
bar character, also called a pipe, |, as a delimiter.

When you import your flashcardz data file into Excel, you will see that the
flashcardz program has modified the data slightly by adding an additional
column, the tally column.


## **Run flashcardz on a web page**

A program named Jupyter Lab allows flashcardz to be run on a web page.
Flashcardz works best when using this Jupyter Lab program!  Jupyter Lab is free
and is easy to install.  It is not included in the basic python package.  To
install do:

`C:\> pip install jupyterlab`

Then to start up Jupyter Lab do:

`C:\> jupyter lab`

More info about Jupyter Lab can be found at [https://jupyter.org/](https://jupyter.org/).
This video can help: [Jupyter Notebook Complete Beginner Guide](https://www.youtube.com/watch?v=5pf0_bpNbkw).

Jupyter Lab is vaguely similar to Microsoft Excel.  Like Excel, Jupyter Lab
contains cells in which data can be entered.  However Jupyter Lab contains only
one column of cells; and the cells are not automatically present.  Each cell
has to be created manually (via selecting appropriate menu commands).

For flashcardz, the first cell should contain `from flashcardz import *`.
Do Ctrl+Enter to run the cell.  Create a new cell and enter one of flashcardz'
functions.  For example: `go()`.  Press Ctrl+Enter to run that cell.
