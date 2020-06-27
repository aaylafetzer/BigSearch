# BigSearch
BigSearch is a simple Python program that recursively indexes the directory tree it's placed in and records the indexes to a SQLite database so massive files can be searched more easily. This was originally designed to help journalists search the BlueLeaks dump for keywords.
## Installation
Install Python from [python.org](https://www.python.org/downloads/) if you're using Windows or this guide from [python-guide.org](https://docs.python-guide.org/starting/install3/osx/) if you're using a Mac. Next:

1. Download and extract BigSearch to the directory you want to index and search
2. Navigate a terminal/command prompt to the directory and run ``pip install -r requirements.txt``
3. Run app.py (``python3 app.py`` if you're running it from the terminal) and the script will begin to index the directory. This will only happen once unless you delete ``BigSearchDB.sqlite``