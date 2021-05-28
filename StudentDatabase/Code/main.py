# For how to import classes from other files in python: c
from StudentDataLoader import StudentDataLoader
from QueryManager import QueryManager
import os

dataBaseLocation = "../chinook.db"

# create student table and load the student data in:
loader = StudentDataLoader(dataBaseLocation)
loader.loadStudentData()

# handle the main menu options now:
queryManager = QueryManager(dataBaseLocation)
queryManager.manageQueryOptions()
