import sqlite3
from InputManager import InputManager

'''

Handles the creation of the Student 
table, and loads the student data into 
that table

'''

class StudentDataLoader:

    dataBaseDirectory = ""
    inputManager = InputManager()

    def __init__(self, databaseDirectory):
        self.dataBaseDirectory = databaseDirectory

    # Referenced from: https://pythonexamples.org/python-sqlite3-check-if-table-exists/
    def checkIfStudentTableExists(self, connection):
        cursor = connection.cursor()
        cursor.execute('''

            SELECT count(name) 
            FROM sqlite_master 
            WHERE (type='table') AND 
                (name = 'Student');

        ''')
        if (cursor.fetchone()[0] == 1):
            # table exists already
            return True

            # table does not exist yet
        return False


    def createTable(self, connection):
        query = '''
        
            CREATE TABLE Student (

                StudentId INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName VARCHAR(35),
                LastName VARCHAR(35),
                GPA REAL,
                Major VARCHAR(45),
                FacultyAdvisor VARCHAR(35),
                Address VARCHAR(35),
                City VARCHAR(35),
                State VARCHAR(35),
                ZipCode VARCHAR(12),
                MobilePhoneNumber VARCHAR(14),
                isDeleted INTEGER

            );
        
        '''
        connection.execute(query)


    def loadStudentData(self):

        '''

            Loads the data from the spreadsheet into
            the database table called Student

        '''
        with open("../students.csv") as file:
            # skip the first line, since first line is just the name of the columns
            file.readline()

            # get the actual data now, which follows after line 1
            data = file.readlines()

        # Form the records: FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA
        records = []
        for i in data[:]:
            # Remove new line characters and separate into individual strings:
            i = i.strip().split(",")

            i[6] = self.inputManager.cleanUpPhoneNumber(i[6])
            records.append(i)

        # load the records into the database:
        connection = sqlite3.connect(self.dataBaseDirectory)

        if (self.checkIfStudentTableExists(connection) == False):
            print("Student Table does not exist, creating it...")
            self.createTable(connection)
        else:
            connection.close()
            print("Student Table already exists, no need to repopulate it.")
            return

        connection.executemany(

            "INSERT INTO Student(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNumber, Major, GPA) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            records

        )

        connection.commit()
        connection.close()
