import os
import json
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

generateFilesList = False

if not os.path.exists("BigSearchDB.sqlite"):
    generateFilesList = True  # Generate the file list for a new database

engine = create_engine("sqlite:///BigSearchDB.sqlite")


class FilePath(Base):
    __tablename__ = "files"

    path = Column(String, primary_key=True)

    def __repr__(self):
        return f"<FilePath(path={self.path})>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Generate the file list
if generateFilesList:
    print("Indexing Files")
    i = 0
    for root, dirs, files in os.walk("."):
        for name in files:
            i += 1
            print(f"Indexed {i} files", end="\r")
            newPath = os.path.join(root, name)
            session.add(
                FilePath(path=newPath)
            )
    print("\nWriting index to database file. This might take a while.")
    session.commit()
    print(f"Indexing Complete")

query = input("Search Query: ")
for file in session.query(FilePath). \
        filter(FilePath.path.ilike(f"%{query}%")):
    print(file.path)
