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

DROP TABLE Student;

SELECT *
FROM Student;
