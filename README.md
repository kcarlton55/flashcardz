# **flashcardz**

## **What the program does**
Flashcardz is used to aid in learning a foreign language, learning math tables,
etc..  The program works by showing the word on each card, then its definition,
to the user one-by-one.  A tally is recorded for each word that the user
correctly remembered the definition of.  Cards are removed once the tally
reaches a maximum value.  (The word "Cards" actually means words and defintions
that are stored in a file on the user's computer.)

The program runs from python's command line terminal.  Use flashcardz primary
function to show the cards:

```
>>> go()
```

Adding words words to your deck of cards is easy.  Use flashcardz's add()
fuction:

```
>>> add('correr', 'to run (to move quickly on two feet)')
```

Words and defintionions can also be imported from an Excel file.


## **Features**
* Cost: Free (as the wind).
* Easy addition of words and defintions via copy and paste.
* User can add links to urls into cards.
* Can import words and definitions from an Excel file.
* Deck of cards is shuffled before each viewing.
* Score kept of number of times the word's definitions are correcty known.
* Card automatically removed once max score has been reached.
* Can highlight portions of text with underscores, italics, or colors.
* flashcardz needs no supporting files. Only the basic python program is needed.


## **How to install**
For this program to run, it requires both python and flashcards.py to be
installed on your computer.  By the way, both are free to install and
use.

To install python, download the program from its home site,
[python.org](https://www.python.org/).  Then install it.  Download version 3.8
or later.

To install flashcardz.py, open a Window's command prompt
([how to open a command prompt](https://www.youtube.com/watch?v=uE9WgNr3OjM),
[command prompt basics](https://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/))
and enter into the command prompt:
```
pip install flashcardz
```
This installs flashcardz on your computer.  Pip is a program is automatically
installed when python gets installed.

Pip (Preferred Installer Program) is used by python to manage python packages
like flashcardz.py.  You can use it to install python packages, uninstall them,
or update them.  There are various sites on the web that describe how to use
pip.  Among them is this site:
[How to use pip](https://note.nkmk.me/en/python-pip-usage/).

Here is how to update flashcardz to the latest version or uninstall it:
```
>>> pip upgrade flashcardz

>>> pip uninstall flashcardz
```

If you do not wish to use pip to install, there is an alternative method
(requires an alternative method to start up flashcardz... see below).
Download flashcardz from its home on github:
[github.com/kcarlton55/flashcardz](https://github.com/kcarlton55/flashcardz).
Click the "Code" button,and then pick "Download zip".  In the zip file that you
downloaded, look in the directory named src and look for the file named
flashcardz.py.  Install it in a directory of your chosing.  (Python is still
required to be on your computer in order to run flashcardz.)


## **How to run flashcardz**

If you used pip to install flashcardz, open a command prompt (described above)
and start up a session of python.  In MS Windows, this is usually done by
entering *py*.  On other operating  systems, enter *python*:

```
C:\Users\Ken> py
Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

In the above example, C:\Users\Ken> is the Windows command prompt that shows on
my computer.  It will be different on yours.  When you execute *py*, python
will show some information reguarding the python version you are using (i.e.
Python 3.12.2 (tags, etc.) You can ignore this.  Then python shows its prompt,
i.e. a chevron (>>>), and then waits for you to enter a command.  Enter your
first command in order to load flashcardz into memory:

```
>>> from flashcardz import *
```

This imports a number of functions that can be used to control the flashcardz
program including add(), cards(), and  go().  Typing help(functions), help(go),
help(cards) etc. will information about what a particular function does.

If you did not use pip to install flashcardz, and instead obtained it from
github.com (described above), then do the following: open up a command prompt,
i.e. a cmd window in the file location where flashcardz.py is located
([Open Command Prompt in Current Folder or Directory](https://www.youtube.com/watch?v=bgSSJQolR0E))
Then from the command prompt, do:

```
C:\Users\Ken> py -i flashcardz.py
```

The *-i* switch causes flashcardz to automatically open in *interacive* mode,
i.e. opens the python termial for input.


To add data for flashcardz, run the add() function like this:

```
>>> add('amigo, amiga nm, nf', '(camarada) friend n buddy n')
```

That is, the structure should be add('my word', 'my definition').  Each time
you use the add() function, the data you enter is added to a data file for
later use.  If you would like to add a multiline defintion, do so like this:

```
>>> add(''''amigo, amiga nm, nf''',
    '''(camarada) friend n buddy n

    Nuestro primer viaje, a Cuzco, lo organizamos entre cuatro amigos.
    We organized our first trip, to Cuzco, among four friends.

    [how to pronounce](https://www.wordreference.com/es/en/translation.asp?spen=amigo)''')
```

You'll notice, to enter a multiline definition, use three quotation marks, ''',
at the beginning and the end of the word and definition.  Don't forget to close
the function by adding a prenthesis at the end.  When you run the go() function,
the defintion above will show as six different lines, including blank lines.
Also note: it is not necessary to type all this data in manually.  The easiest
thing to do is to copy and paste from the site that has a dictionary for the
language you are learning.

Notice the last line in the defintion.  It is a URL link.  URL links are
inserted into a word's definition using brackets and parenthesis using the
format ```[link description](URL)```


When you're ready to view the cards one-by-one, and ready to try to figure out
the definition of each word, run the go() function:

```
go()
```

When the go() function is run, it automatically opens up the data file that
contains your words and definions so that the information from it can be
presented to you.  When the go() function completes its task, tallies are
updated, and if that maximum tally for any word has been reached, that card is
removed from the deck

When you want to exit python, enter either quit() or exit() or Ctrl+D (or quit
or exit for python 3.13 and up):

```
quit()
```

## **Convert an Excel file to a flashcardz data file**

Words and definitions can be created in an Excel and then exported to a text
file that flashcardz can open and read.  First, in cells A1 and B1 of the Excel
file enter the column headers.  Use as column headers "word" and "definition"
(without the quotation marks) for these two cells.  In  subsequent rows, 2, 3,
etc. put your words and their defintions.

Now you are ready to export to a text file.  The text file must be in a format
called csv. If you are not aware of this file format, please see this
explanation: [Comma-separated values](https://en.wikipedia.org/wiki/Comma-separated_values)
Futhermore UTF-8 character encoding is required.  In Excel, when you do a
Save As, look for "CSV UTF-8 (Comma delimitd)(*.csv)".  (However, read on...
a bug exists.)

There is a problem using the normal way that Excel exports to a csv file.  The
csv file that Excel exports to will have columns (i.e. the word and defintion
columns) separated by commas.  But many times, like shown in the "add" example
above, commas will be present in the definition.  This will result in
flashcardz interpreting that data as having additional columns; columns that
shouldn't exist.  This will cause the flashcardz program to crash.

To remedy this situation, flashcardz was instead coded to recognize the
pipe, i.e. vertical bar character, |, as the separator (more specifcally called
a delimiter).  Excel was somewhat poorly designed because Excel does not allow
to change to a different delimiter when exporting.  But there is a relatively
easy work-around.  See this youtube video for how to do it:
[Export Data with Pipe Delimiters Instead of Commas](https://www.youtube.com/watch?v=jieWzHJjVBU)

## **Opening a flashcardz data file into Excel**

Opening a flashcardz data file into Excel is relatively easy.  When you open a
flashcardz data file (with a csv or txt extension), you will be given the
option to use a different delimiter other than a comma.  Use the vertical
bar character, also called a pipe, |, as a delimiter.

When you import your flashcardz data file into Excel, you will see that the
flashcardz program has modified the data slightly by adding and additional, the
tally column.





