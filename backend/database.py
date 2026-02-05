import sqlite3
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

class Database:

    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()


    def creatTableUser(self):
        self.cursor.execute("DROP TABLE IF EXISTS user")
        table_creation_query = """
        CREATE TABLE user (
            userid TEXT NOT NULL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            classname TEXT NOT NULL,
            major TEXT NOT NULL,
            email TEXT NOT NULL,
            role INT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True



    def creatTableGrade(self):
        self.cursor.execute("DROP TABLE IF EXISTS grade")
        table_creation_query = """
        CREATE TABLE grade (
            userid TEXT NOT NULL,
            grade INT,
            message TEXT,
            fileid TEXT,
            eventid NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableAbsence(self):
        self.cursor.execute("DROP TABLE IF EXISTS absence")
        table_creation_query = """
        CREATE TABLE absence (
            userid TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            excused INT not NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableSchedule(self):
        self.cursor.execute("DROP TABLE IF EXISTS schedule")
        table_creation_query = """
        CREATE TABLE schedule (
            courseid TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            change INT not NULL,
            major TEXT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return True

    def creatTableToken(self):
        self.cursor.execute("DROP TABLE IF EXISTS token")
        tableCreationQuery = """
        CREATE TABLE token (
            userid TEXT NOT NULL,
            token TEXT NOT NULL,
            creattime INTEGER NOT NULL
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True

    # Nicht mehr in gebrauch
    def creatTableSubject(self): 
        self.cursor.execute("DROP TABLE IF EXISTS subject")
        """
        tableCreationQuery = 
        #CREATE TABLE subject (
        #    listofteachers TEXT NOT NULL,
        #    name TEXT NOT NULL,
        #    listofstudents TEXT NOT NULL
        #);
        """
        #self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True



    def creatTableCourse(self):
        self.cursor.execute("DROP TABLE IF EXISTS course")
        tableCreationQuery = """
        CREATE TABLE course (
            courseid TEXT NOT NULL,
            userid TEXT NOT NULL,
            subject TEXT NOT NULL,
            courseName TEXT NOT NULL            
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True
    
    def creatTableExamen(self):
        self.cursor.execute("DROP TABLE IF EXISTS examen")
        tableCreationQuery = """
        CREATE TABLE examen (
            courseid TEXT NOT NULL,
            testname TEXT NOT NULL,
            weight INT NOT NULL,
            eventid TEXT NOT NULL,
            changedatum TEXT NOT NULL            
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True

    def creatTableEvent(self):
        self.cursor.execute("DROP TABLE IF EXISTS event")
        tableCreationQuery = """
        CREATE TABLE event (
            eventid TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            describtion TEXT,
            type INT            
        );
        """

        # type Exam = 666
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True


    def creatTableFile(self):
        self.cursor.execute("DROP TABLE IF EXISTS file")
        tableCreationQuery = """
        CREATE TABLE file (
            fileid TEXT NOT NULL,
            namebefor TEXT NOT NULL,
            nameafter TEXT NOT NULL
        );
        """
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True

    def passwordHashAndSalt(self,password):
        return password

    def addNewFile(self,nameOfFile):
        sql = "INSERT INTO file (fileid,namebefor,nameafter) VALUES (?,?,?)"

        fileId = str(uuid.uuid4())
        newFileName = str(uuid.uuid4())
        self.cursor.execute(sql, (fileId,nameOfFile,newFileName))
        output = self.cursor.fetchone()
        self.conn.commit()
        return fileId, newFileName

    def deleteFile(self,fileId):
        sql = "DELETE FROM file WHERE fileid = ?"
        self.cursor.execute(sql, (fileId,))
        output = self.cursor.fetchone()
        self.conn.commit()
        return True

    def getNamesOfFile(self,fileId):
        sql = "SELECT nameafter,namebefor FROM file WHERE fileid = ?"

        self.cursor.execute(sql, (fileId,))
        output = self.cursor.fetchone()
        self.conn.commit()
        nameBefor = output[0][0]
        nameAfter = output[0][1]

        
        return nameBefor, nameAfter

    def readAndReturnTableFile(self):
        self.cursor.execute("SELECT * FROM file")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output



    def readAndReturnTableUser(self):
        self.cursor.execute("SELECT * FROM user")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableGrade(self):
        self.cursor.execute("SELECT * FROM grade")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableAbsence(self):
        self.cursor.execute("SELECT * FROM absence")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def readAndReturnTableSchedule(self):
        self.cursor.execute("SELECT * FROM schedule")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output




    def isUserValid_getUserID(self, username, password):
        sql = "SELECT password,userid FROM user WHERE username = ?"
        self.cursor.execute(sql, (username,))
        output = self.cursor.fetchall()
        self.conn.commit()

        

        if output == []:
            return False

        ph = PasswordHasher()
        try:
            ph.verify(output[0][0], password)
        except VerifyMismatchError:
            return False

        return output[0][1]

    def isUserExist(self,username):
        sql = "SELECT COUNT(*) FROM user WHERE username = ?"
        self.cursor.execute(sql, (username,))
        output = self.cursor.fetchone()
        self.conn.commit()

        if output[0] == 1:
            return True
        return False

    def addNewUser(self,username,password,classname,major,email,role,firstName, lastName):

        if self.isUserExist(username):
            return False


        sql = "INSERT INTO user (userid,username,password,classname,major,email,role,firstname,lastname) VALUES (?,?,?,?,?,?,?,?,?)"
        userID = str(uuid.uuid4())
        self.cursor.execute(sql, (userID,username,password,classname,major,email,role,firstName,lastName))
        self.conn.commit()

        
        return userID

    def addNewCourse(self,courseID,userID,subject,courseName):
        sql = "INSERT INTO course (courseid,userid,subject,courseName) VALUES (?,?,?,?)"
        self.cursor.execute(sql, (courseID,userID,subject,courseName))
        self.conn.commit()
        return True
    def addNewExamen(self,courseID, eventID, testName,weight):
        sql = "INSERT INTO examen (courseid,eventid,testname,weight,changedatum) VALUES (?,?,?,?, DATETIME('now'))"
        self.cursor.execute(sql, (courseID,eventID,testName,weight))
        self.conn.commit()
        return True

    def addNewGrade(self,userID,eventID,grade = 0,message = "", fileID = "",):
        sql = "INSERT INTO grade (userid,eventid,grade,message,fileid) VALUES (?,?,?,?,?)"
        self.cursor.execute(sql, (userID,eventID,grade,message,fileID))
        self.conn.commit()
        return True

    def addNewEvent(self,eventID,location,date,starttime,endtime,describtion,kind):
        sql = "INSERT INTO event (eventid, location, date, starttime, endtime, describtion, type) VALUES (?,?,?,?,?,?,?)"
        self.cursor.execute(sql, (eventID,location,date, starttime, endtime, describtion, kind))
        self.conn.commit()
        return True
    
    def addNewGradesForExamForEveryoneInCourse(self,courseID,eventID):
        sql = """INSERT INTO grade (userid, eventid, grade, message, fileid)
            SELECT userid, ?, 0, '',''
            FROM course
            WHERE courseID = ?;
            """    
        self.cursor.execute(sql, (eventID,courseID))
        self.conn.commit()
        return True

    def changeGradeWithUserIDandEventID(self, userID, eventID, grade, message,fileID):
        sql = """UPDATE grade
        SET grade = ?,
            message = ?,
            fileid = ?
        WHERE userid = ?
            AND eventid = ?;        
        """

        self.cursor.execute(sql, (grade, message, fileID, userID, eventID))
        self.conn.commit()
        return True


    
    def changePassword(self,userID,password,newPassword):
        sql = "SELECT password FROM user WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchone()

        self.conn.commit()

        if output == []:
            return False

        dbPassword  = output[0]


        ph = PasswordHasher()
        try:
            ph.verify(dbPassword, password)
        except VerifyMismatchError:
            return False

        hashedNewPassword = ph.hash(newPassword)

        sql = "UPDATE user set password = ? WHERE userid = ?"
        self.cursor.execute(sql, (hashedNewPassword,userID))
        self.conn.commit()

        return True



        

        








    def addNewToken(self,userid):
        sql = "INSERT INTO token (userid,token,creattime) VALUES (?,?,strftime('%s', 'now'))"
        token = str(uuid.uuid4())


        self.cursor.execute(sql, (userid,token))
        output = self.cursor.fetchone()
        self.conn.commit()
        return token


    def getUseridFromToken(self,token):
        #funktion return False if no userid exist or the token is invalid

        countOfNumbersUntilTokenIsInvalid = 20
        sql = "SELECT * FROM token WHERE token = ? AND creattime > (strftime('%s', 'now') - ?*60)"
        self.cursor.execute(sql, (token,countOfNumbersUntilTokenIsInvalid))
        output = self.cursor.fetchall()
        self.conn.commit()


        if output == []:
            return False

        return output[0][0]


    def deletOldTokens(self):
        countOfNumbersUntilTokenIsInvalid = 20
        sql = "DELETE FROM token WHERE creattime < (strftime('%s', 'now') - ?*60"
        self.cursor.execute(sql, (countOfNumbersUntilTokenIsInvalid,))
        self.conn.commit()

    def deletToken(self,token):
        sql = "DELETE FROM token WHERE token = ?"
        self.cursor.execute(sql, (token,))
        self.conn.commit()
        return

    def getAllUserDataWithUserID(self,userID):
        sql = "SELECT * FROM user WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output



    def getALLCourseWithUserID(self,userID):
        sql = "SELECT courseid,subject,courseName FROM course WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output


    def getAllExamsFromCourseID(self,courseID):
        sql = """SELECT 
        ex.testname, 
        ex.weight,
        ev.date,
        ex.eventid
        FROM examen AS ex
        INNER JOIN event AS ev
            ON ex.eventid = ev.eventid
        WHERE courseid = ?;
        """
        self.cursor.execute(sql, (courseID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output

    def getAllGradesWithCourseIDAndUserID(self,courseID, userID):
        sql = """
            SELECT 
                ex.testname, 
                ex.weight, 
                g.grade,
                g.message,
                g.fileId,
                ev.date
            FROM examen AS ex
            LEFT JOIN grade AS g
                ON g.eventid = ex.eventid
                AND g.userid = ?
            INNER JOIN event AS ev
                ON ev.eventid = ex.eventid
            WHERE ex.courseid = ?;
            """
        self.cursor.execute(sql,(userID, courseID))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output
    
    def getRolefromUserWithUserID(self,userID):
        sql = "SELECT role FROM user WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output[0][0]

    def isUserIDinCourse(self,userID,courseID):
        sql =     sql = """SELECT CASE
            WHEN EXISTS (
                SELECT 1
                FROM course
                WHERE userid = ?
                    AND courseid = ?
            )
            THEN 1
            ELSE 0
            END;
        """
       
        self.cursor.execute(sql, (userID, courseID))
        output = self.cursor.fetchone()[0] 
        self.conn.commit()

        if output == 1:
            return True
        return False

    def getAllGradesPlusNamesWithEventID(self,eventID):
        sql = """
            SELECT 
                u.firstname,
                u.lastname,
                g.grade,
                g.message,
                g.fileid
            FROM grade AS g
            INNER JOIN user AS u
                ON g.userid = u.userid
            WHERE g.eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def getAllExamAndEventDataWithEventID(self,eventID):
        sql = """
            SELECT 
                ex.testname,
                ex.weight,
                ev.location,
                ev.date,
                ev.starttime,
                ev.endtime,
                ev.describtion
            FROM examen AS ex
            INNER JOIN event AS ev
                ON ex.eventid = ev.eventid
            WHERE ex.eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output[0]



    """
    creatTableUser()
    insertTestDataTableUser()
    print(readAndReturnTableUser())

    print(isUserValid("Emil","Emil"))
    addNewUser("Gremaud","Gremaud","M4i","Lehrer MA")
    print(readAndReturnTableUser())

    print(isUserValid("Gremaud","Gremaud"))

    #creatTableToken()

    #addNewToken("eliah")


    print(getUseridFromToken("eliah"))
    #creatTableFile()


    print(readAndReturnTableFile())
    #deleteFile("d1072a26-6feb-44b0-bbec-843e00c387bb")
    print(readAndReturnTableFile())

    """

    #print(isUserValid_getUserID("Eliah","Eliah"))

