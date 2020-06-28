import os
import argparse

# File processing imports
import csv
import PyPDF2
import re

# SQL Alchemy imports
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Command line argument handling
parser = argparse.ArgumentParser(description="Search a large directory tree")
parser.add_argument("-r", "--regex", help="Allow any regular expression to be entered", action="store_true")
parser.add_argument("-v", "--verbose", help="Print file names as they're indexed as opposed to a counter",
                    action="store_true")
group = parser.add_argument_group("File Options")
group.add_argument("-c", "--csv", help="Store/search the contents of csv files in database", action="store_true")
group.add_argument("-p", "--pdf", help="Store/search the contents of pdf files in database", action="store_true")
parser.add_argument("query", help="Query to search for")

args = parser.parse_args()

Base = declarative_base()

generateFilesList = False

if not os.path.exists("BigSearchDB.sqlite"):
    generateFilesList = True  # Generate the file list for a new database

engine = create_engine("sqlite:///BigSearchDB.sqlite")


class FilePath(Base):
    """
    File path for indexing files in database
    """
    __tablename__ = "FilePaths"

    path = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<FilePath(path={self.name})>"

    def __init__(self, path, name):
        self.path = path
        self.name = name


class CsvFile(Base):
    """
    CSV Files and their contents for searching
    """
    __tablename__ = "CsvFiles"

    path = Column(String, primary_key=True)
    content = Column(String)

    def __repr__(self):
        return f"<CsvFile(path={self.path}>"

    def __init__(self, path):
        self.path = path
        with open(self.path, "r") as openFile:
            self.content = openFile.read()


class PdfFile(Base):
    """
    PDF File Paths and their contents for searching
    """
    __tablename__ = "PdfFiles"

    path = Column(String, primary_key=True)
    content = Column(String)

    def __repr__(self):
        return f"<PdfFile(path={self.path}>"

    def __init__(self, path):
        self.path = path
        content = ""
        pdfFile = PyPDF2.PdfFileReader(path)
        pdfPages = pdfFile.numPages
        for n in range(0, pdfPages):
            page = pdfFile.getPage(i)
            pageText = page.extractText()
            content += pageText
        self.content = content


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Generate the database
if generateFilesList:
    print("Indexing Files")
    i = 0
    for root, dirs, files in os.walk("."):
        for name in files:
            i += 1
            if args.verbose:
                print(f"Indexed {i} files: {name}")
            else:
                print(f"Indexed {i} files", end="\r")
            newPath = os.path.join(root, name)
            newPathName, newPathExtension = os.path.splitext(newPath)
            # Add file path to database
            session.add(
                FilePath(newPath, newPathName)
            )
            # Add csv file to database if enabled
            if args.csv and newPathExtension == ".csv":
                session.add(
                    CsvFile(newPath)
                )
            # Add pdf file content to database if enabled
            if args.pdf and newPathExtension == ".pdf":
                session.add(
                    PdfFile(newPath)
                )
    print("\nWriting index to database file. This might take a while.")
    session.commit()
    print(f"Indexing Complete")

# Search the database
if args.regex:
    query = args.query
else:
    query = f"%{args.query}%"  # Basic regex search if the user doesn't set the --regex flag

print(f"Search Query: {args.query}")

print("-" * 15 + "Filenames" + "-" * 15)
fileMatches = False
for file in session.query(FilePath). \
        filter(FilePath.name.ilike(query)):
    fileMatches = True
    print(file.path)
if not fileMatches:
    print("Query was not found in any filenames")

# Search through pdf files if requested
if args.pdf:
    print("-" * 15 + "PDF Files" + "-" * 15)
    fileMatches = False
    for file in session.query(PdfFile). \
            filter(PdfFile.content.ilike(query)):
        print(file.path)
        fileMatches = True
    if not fileMatches:
        print("Query was not found in any PDF files")

# Search through csv files if requested
if args.csv:
    print("-" * 15 + "CSV Files" + "-" * 15)
    fileMatches = False
    for file in session.query(CsvFile). \
            filter(CsvFile.content.ilike(query)):
        print(file.path)
        fileMatches = True
    if not fileMatches:
        print("Query was not found in any CSV files")
