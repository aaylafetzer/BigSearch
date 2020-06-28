# BigSearch
BigSearch is a simple Python program that recursively indexes the directory tree it's placed in and records the indexes to a SQLite database so massive files can be searched more easily. This was originally designed to help journalists search the BlueLeaks dump for keywords.
## Installation
Install Python from [python.org](https://www.python.org/downloads/) if you're using 
Windows or from the App Store if you're using a Mac.

1. Download and extract BigSearch to the directory you want to index and search
2. Navigate a terminal/command prompt to the directory and run ``pip install -r requirements.txt``
3. Run app.py (``python3 app.py`` if you're running it from the terminal) and the script will begin to index the directory. This will only happen once unless you delete ``BigSearchDB.sqlite``

## Advanced Usage
To get started using BigSearch, simply run ``python3 app.py`` after installing the 
requirements and the rest will be handled for you. However, there are more advanced use
options of BigSearch if you want to get more data or dig deeper. To access them, you can
use these command line arguments

- ``-r / --regex`` Will allow you to search for any regular expression, as opposed to the 
default ``%query%``
- ``-c / --csv`` Will save the contents of all .csv files into the database to enable searching
them quickly
- ``-p / --pdf`` Will use pdftotext to attempt to read the text content of all pdf files and
save it to the database to enable searching them quickly. Be aware, because of the [limitations](https://stackoverflow.com/a/17099530/13026048)
of converting PDF files to text files, this is not guaranteed to be an accurate search, but has the potential to be useful when
searching dumps of PDF files generated in software like Microsoft Word (as opposed to read by a scanner, etc.)