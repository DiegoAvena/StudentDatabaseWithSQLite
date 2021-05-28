import sqlite3
from InputManager import InputManager

'''

Handles the behavior of all 
of the actions the user can 
perform on the Students table 

'''
class QueryManager:

    dataBaseDirectory = ""
    connection = None
    inputManager = InputManager()

    def __init__(self, dataBaseDirectory):
        self.dataBaseDirectory = dataBaseDirectory

    def makeSureToDisconnect(self):
        if (self.connection != None):
            self.connection.close()


    def makeSureConnectionIsEstablished(self):
        if self.connection == None:
            # establish the connection:
            self.connection = sqlite3.connect(self.dataBaseDirectory)


    def displayResultsOfQuery(self, cursor):
        print(
            "StudentID | Firstname | Lastname | GPA | Major | Faculty Advisor | Address | City | State | Zipcode | MobilePhoneNumber |")
        for row in cursor:
            record = ""
            for column in row:
                record += str(column)
                record += " | "
            print(record)

    # Displays all of the records in the students table
    def displayAll(self):
        self.makeSureConnectionIsEstablished()
        query = '''
        
            SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, Zipcode, MobilePhoneNumber 
            FROM Student
            WHERE (isDeleted IS 0) || (isDeleted IS NULL);
        
        '''
        cursor = self.connection.execute(query)

        # display the results:
        self.displayResultsOfQuery(cursor)

    # allows the user to add new students in
    def addNewStudents(self):

        self.makeSureConnectionIsEstablished()
        newRecords = []

        while True:
            newRecord = []
            newRecord.append(self.inputManager.obtainText("Enter the first name of the student: "))
            newRecord.append(self.inputManager.obtainText("Enter the last name of the student: "))
            newRecord.append(self.inputManager.obtainDecimalNumber("Enter the students GPA: ", 0))
            newRecord.append(self.inputManager.obtainText("Enter the students major: "))
            newRecord.append(self.inputManager.obtainText("Enter the name of the faculty advisor for this student: "))
            newRecord.append(self.inputManager.obtainText("Enter the address this student lives at: "))
            newRecord.append(self.inputManager.obtainText("Enter the city this student lives at: "))
            newRecord.append(self.inputManager.obtainText("Enter the state this student lives at: "))
            newRecord.append(self.inputManager.obtainZipCode("Enter the zipcode this student lives at: "))
            newRecord.append(self.inputManager.obtainPhoneNumber("Enter the phone number for this student: "))
            newRecords.append(newRecord)

            print("Student created.")
            rawUserResponse = input("Enter 2 to add another student, or enter anything else to confirm.")
            try:

                cleanedUserResponse = int(rawUserResponse)
                if (cleanedUserResponse != 2):
                    # confirm and add the record into the table
                    break
            except ValueError:
                # confirm and add the record into the table
                break

        query = '''
        
            INSERT INTO Student(FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        
        '''
        self.connection.executemany(query, newRecords)
        self.connection.commit()

        if (len(newRecords) > 1):
            print("NEW RECORDS ADDED!")
        else:
            print("NEW RECORD ADDED!")

        print()

    '''
    
    makes sure the ID the user gave is an ID for a student 
    that currently exists in the Student table
    
    For organization this method should 
    be placed in the InputManager with the
    rest of the input validation methods, 
    but I decided on placing it here because 
    it requires a direct interaction with the 
    database, requiring a connection, and I did 
    not want to bother with making another 
    connection to the database from another file
    
    '''
    def validateStudentID(self, studentIDToValidate):
        cursor = self.connection.execute("SELECT COUNT(*) FROM Student;")
        totalRecords = cursor.fetchone()[0]
        if ((studentIDToValidate > totalRecords) or (studentIDToValidate < 1)):
            return False
        else:
            cursor = self.connection.execute("SELECT isDeleted FROM Student WHERE StudentID = ?;", [studentIDToValidate])

            for i in cursor:
                studentIsDeleted = i[0]
                break

            if (studentIsDeleted == None) or (studentIsDeleted != 1):
                return True

            return False

    # Allows the user to delete students
    def deleteStudents(self):
        self.makeSureConnectionIsEstablished()
        while(True):
            rawUserInput = input("Enter the ID for the student you wish to delete: ")
            try:
                studentID = int(rawUserInput)

                if self.validateStudentID(studentID):
                    cursor = self.connection.execute("SELECT FirstName, LastName FROM Student WHERE StudentID = ?;", [studentID])
                    studentName = cursor.fetchone()
                    rawUserInput = input("Are you sure you want to delete student with name: " + studentName[0] + " " + studentName[1] + "? enter y to confirm and anything else to cancel.")

                    if (rawUserInput.lower() == 'y'):
                        query = '''

                                                UPDATE Student
                                                SET isDeleted = 1
                                                WHERE StudentID = ?;

                                            '''
                        self.connection.execute(query, [studentID])
                        self.connection.commit()
                        rawUserInput = input("Student deleted. Would you like to delete another student? Enter y for yes and anything else for no.")
                        if (rawUserInput.lower() != 'y'):
                            break
                    else:
                        rawUserInput = input("Deletion cancelled. Would you like to delete a student still? Enter y for yes and anything else for no.")
                        if (rawUserInput.lower() != 'y'):
                            break
                else:
                    print("There is no student with that ID, try another one.")
            except ValueError:
                print("Student ID must be an integer, try again.")

    # allows the user to update student information: major, advisor, or phone number
    def updateStudents(self):
        self.makeSureConnectionIsEstablished()
        while(True):
            rawUserInput = input("Enter the ID for the student you wish to update: ")
            try:
                studentID = int(rawUserInput)

                if self.validateStudentID(studentID):

                    cursor = self.connection.execute("SELECT FirstName, LastName FROM Student WHERE StudentID = ?;", [studentID])
                    studentName = cursor.fetchone()
                    print("Updating information for: " + studentName[0] + " " + studentName[1])
                    prompts = ["Would you like to update his or her major? (y/n)",
                               "Would you like to update his or her advisor? (y/n)",
                               "Would you like to update his or her phone number? (y/n)"]
                    for i in range(0, 3):
                        userInput = input(prompts[i])
                        if (userInput == 'y'):
                            if (i == 0):
                                newMajor = self.inputManager.obtainText("Enter the new major: ")
                                query = '''

                                    UPDATE Student 
                                    SET Major = ?
                                    WHERE StudentID = ?;

                                '''
                                self.connection.execute(query, [newMajor, studentID])
                                self.connection.commit()
                            elif (i == 1):
                                newAdvisor = self.inputManager.obtainText("Enter the new advisor: ")
                                query = '''

                                    UPDATE Student 
                                    SET FacultyAdvisor = ? 
                                    WHERE StudentID = ?;

                                '''
                                self.connection.execute(query, [newAdvisor, studentID])
                                self.connection.commit()
                            else:
                                newPhoneNumber = self.inputManager.obtainPhoneNumber("Enter the new phone number: ")
                                query = '''

                                    UPDATE Student
                                    SET MobilePhoneNumber = ? 
                                    WHERE StudentID = ?;

                                '''
                                self.connection.execute(query, [newPhoneNumber, studentID])
                                self.connection.commit()

                    userinput = input("Would you like to update another student? Enter y for yes, and anything else for no")
                    if (userinput.lower() != 'y'):
                        break

                else:
                    print("Student with that ID does not exist, try another ID.")
            except ValueError:
                print("This ID must be an integer")

    # Allows the user to query by major, advisor, GPA, city, and state
    def searchAndDisplayByMajorGPACityStateAndAdvisor(self):
        self.makeSureConnectionIsEstablished()

        thereIsAQueryToPerform = False

        query = '''
            
            SELECT StudentID, FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, Zipcode, MobilePhoneNumber
            FROM Student
            WHERE'''

        queryInputs = []

        rawUserResponse = input("Would you like to search by major? (y for yes, anything else for no)")
        if rawUserResponse == 'y':
            major = self.inputManager.obtainText("Enter the major for students you want to look at: ")
            thereIsAQueryToPerform = True
            query += " (Major = ?)"
            queryInputs.append(major)

        rawUserResponse = input("Would you like to search by advisor? (y for yes and anything else for no): ")
        if rawUserResponse == 'y':
            advisor = self.inputManager.obtainText("Enter the advisor for students you want to look at: ")

            if (thereIsAQueryToPerform):
                query += " AND (FacultyAdvisor = ?)"
            else:
                thereIsAQueryToPerform = True
                query += " (FacultyAdvisor = ?)"

            queryInputs.append(advisor)

        rawUserResponse = input("Would you like to search by GPA? (y for yes, and anything else for no): ")
        if rawUserResponse == 'y':
            GPA = self.inputManager.obtainDecimalNumber("Enter the GPA for students you want to look at: ", 0)

            if (thereIsAQueryToPerform):
                query += " AND (GPA = ?)"
            else:
                thereIsAQueryToPerform = True
                query += (" (GPA = ?)")

            queryInputs.append(GPA)

        rawUserResponse = input("Would you like to search by city? (y for yes, and anything else for no)")
        if (rawUserResponse == 'y'):
            city = self.inputManager.obtainText("Enter the city for students you want to look at: ")

            if (thereIsAQueryToPerform):
                query += " AND (City = ?)"
            else:
                thereIsAQueryToPerform = True
                query += " (City = ?)"

            queryInputs.append(city)

        rawUserResponse = input("Would you like to search by state? (y for yes, and anything else for no)")
        if (rawUserResponse == 'y'):
            state = self.inputManager.obtainText("Enter the state for students you want to look at: ")

            if (thereIsAQueryToPerform):
                query += " AND (State = ?)"
            else:
                thereIsAQueryToPerform = True
                query += " (State = ?)"

            queryInputs.append(state)

        # makes sure deleted students are not shown
        query += " AND ((isDeleted IS 0) OR (isDeleted IS NULL));"

        if (thereIsAQueryToPerform):
            print()
            cursor = self.connection.execute(query, queryInputs)
            self.displayResultsOfQuery(cursor)
            print()

    # presents to the user the main menu
    def manageQueryOptions(self):

        while(True):
            print("Select an option.")
            print("Enter 1 to display all Students and their attributes.")
            print("Enter 2 to add new students.")
            print("Enter 3 to update students")
            print("Enter 4 to delete a student")
            print("Enter 5 to search/display students by Major, GPA, City, State, and Advisor")
            print("Enter anything else to quit the app")

            rawUserResponse = input("Enter your choice: ")

            # To review on error handling on python, I referenced:
            try:

                cleanedUpUserResponse = int(rawUserResponse)

                if (cleanedUpUserResponse == 1):
                    self.displayAll()
                elif(cleanedUpUserResponse == 2):
                    self.addNewStudents()
                elif(cleanedUpUserResponse == 3):
                    self.updateStudents()
                elif(cleanedUpUserResponse == 4):
                    self.deleteStudents()
                elif(cleanedUpUserResponse == 5):
                    self.searchAndDisplayByMajorGPACityStateAndAdvisor()
                else:
                    print("Bye!")
                    self.makeSureToDisconnect()
                    break
            except ValueError:
                print("Bye!")
                self.makeSureToDisconnect()
                break
