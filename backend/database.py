import sqlite3
import uuid
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError






class FcmToken:

    conn = None
    cursor = None

    def __init__(self):
        return
    
    def creatTableFcmToken(self):
        self.cursor.execute("DROP TABLE IF EXISTS fcmtoken")
        table_creation_query = """
        CREATE TABLE fcmtoken (
            userid TEXT NOT NULL,
            fcmtoken TEXT NOT NULL,
            hardwaretoken TEXT NOT NULL
        );
        """
        self.cursor.execute(table_creation_query)
        self.conn.commit()
        return


    def addNewFcmToken(self,userID,fcmToken,hardwareToken):
        sql = "INSERT INTO fcmtoken (userid,fcmtoken,hardwaretoken) VALUES (?,?,?)"
        self.cursor.execute(sql, (userID,fcmToken,hardwareToken))
        self.conn.commit()
        return True


    def updateFcmTokenWithUserIDAndHardwareToken(self,userID,fcmToken,hardwareToken):
        sql = """
            UPDATE fcmtoken
                SET fcmToken = ?
            WHERE userid = ?
                AND hardwaretoken = ?;
            """
        self.cursor.execute(sql,(fcmToken,userID,hardwareToken))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def isFcmTokenExistWithUserIDandHardwareID(self,userID,hardwareToken):
        sql = """
            SELECT EXISTS(
                SELECT 1
                FROM fcmtoken
                WHERE userid = ? 
                    AND hardwareid = ?
            );
            """
        self.cursor.execute(sql,(userID,hardwareToken))
        output = bool(self.cursor.fetchone()[0])
        self.conn.commit()
        return output

    def getAllFcmTokenFromUserID(self,userID):
        sql = """
            SELECT (fcmtoken,hardwaretoken) 
            FROM fcmtoken
            WHERE userid = ?;
    
            """
        self.cursor.execute(sql,(userID,))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def deleteFcmTokenWithUserIDAndHardwareID(self,userID,hardwareID):
        sql = """
        DELETE
        FROM fcmtoken
        WHERE userid = ? 
            And hardwareid = ?;
        """

        self.cursor.execute(sql,(userID,hardwareToken))
        output = bool(self.cursor.fetchone()[0])
        self.conn.commit()
        return output



class Token:

    conn = None
    cursor = None

    def __init__(self):
        return


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







class User:

    conn = None
    cursor = None

    def __init__(self):
        return


    
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
            lastname TEXT NOT NULL,
            notifabsenceofteachertoday INT,
            notifabsenceofteachertomorrow INT,
            notifexamtomorrow INT,
            notifeventtomorrow INT,
            notifabsenceduetomorrow INT,
            birthdate TEXT,
            childuserid TEXT
        );
        """
        self.cursor.execute(table_creation_query)
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

    def addNewUser(self,username,password,classname,major,email,role,firstName, lastName,birthDate = None,childUserID = None):

        if self.isUserExist(username):
            return False


        sql = "INSERT INTO user (userid,username,password,classname,major,email,role,firstname,lastname,birthdate,childuserid) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        userID = str(uuid.uuid4())
        self.cursor.execute(sql, (userID,username,password,classname,major,email,role,firstName,lastName,birthDate,childUserID))
        self.conn.commit()

        
        return userID



    def getAllUserDataWithUserID(self,userID):
        sql = """
        SELECT username,classname,major,email,role,firstname,lastname,
        notifabsenceofteachertoday,notifabsenceofteachertomorrow,notifexamtomorrow,notifeventtomorrow,notifabsenceduetomorrow
        FROM user WHERE userid = ?
        """
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchone()


        return list(output)

    def getBirthdateWithUserID(self,userID):
        sql = """
        SELECT birthdate
        FROM user WHERE userid = ?
        """
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchone()
        return output[0]

    def getChildUserIDWithParentUserID(self,userID):
        sql = """
        SELECT childuserid
        FROM user WHERE userid = ?
        """
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchone()
        return output[0]

    def updateUserDataFromUserWithUserID(self,userID,userName, email, notifAbsenceOfTeacherToday,notifAbsenceOfTeacherTomorrow, notifExamTomorrow, notifEventTomorrow,  notifAbsenceDueTomorrow):

        sql = """
        UPDATE user
        SET username =?,
            email =?,
            notifabsenceofteachertoday =?,
            notifabsenceofteachertomorrow =?,
            notifexamtomorrow =?,
            notifeventtomorrow =?,
            notifabsenceduetomorrow =?
        WHERE userid = ?
        """
        self.cursor.execute(sql, (userName, email,notifAbsenceOfTeacherToday, notifAbsenceOfTeacherTomorrow, notifExamTomorrow, notifEventTomorrow,notifAbsenceDueTomorrow,userID))
        self.conn.commit()
        return



    def readAndReturnTableUser(self):
        self.cursor.execute("SELECT * FROM user")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def getRolefromUserWithUserID(self,userID):
        sql = "SELECT role FROM user WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output[0][0]

class File:

    conn = None
    cursor = None

    def __init__(self):
        return
    
    def creatTableFile(self):
        self.cursor.executescript("DROP TABLE IF EXISTS file; DROP TABLE IF EXISTS filepermission")
        tableCreationQuery = """
        CREATE TABLE file (
            fileid TEXT NOT NULL,
            namebefor TEXT NOT NULL,
            nameafter TEXT NOT NULL
        );
        CREATE TABLE filepermission (
            fileid TEXT NOT NULL,
            userid TEXT NOT NULL
        );
        """
        self.cursor.executescript(tableCreationQuery)
        self.conn.commit()
        return True


    def addNewFile(self,nameOfFile):
        sql = "INSERT INTO file (fileid,namebefor,nameafter) VALUES (?,?,?)"

        fileId = str(uuid.uuid4())
        newFileName = str(uuid.uuid4())
        self.cursor.execute(sql, (fileId,nameOfFile,newFileName))
        output = self.cursor.fetchone()
        self.conn.commit()
        return fileId, newFileName

    def addNewFilePermission(self,fileID,userID):
        sql = "INSERT INTO filepermission (fileid,userid) VALUES (?,?)"
        self.cursor.execute(sql, (fileID,userID))
        self.conn.commit()
        return

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


class Grade:

    conn = None
    cursor = None

    def __init__(self):
        return  

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

    def readAndReturnTableGrade(self):
        self.cursor.execute("SELECT * FROM grade")
        output = self.cursor.fetchall()
        self.conn.commit()
        return output

    def addNewGrade(self,userID,eventID,grade = 0,message = "", fileID = "",):
        sql = "INSERT INTO grade (userid,eventid,grade,message,fileid) VALUES (?,?,?,?,?)"
        self.cursor.execute(sql, (userID,eventID,grade,message,fileID))
        self.conn.commit()
        return True


    def updateGradeWithEventIDAndUserID(self,grade,message,fileID,eventID,userID):
        sql = """
            UPDATE grade
                SET grade = ?,
                    message = ?,
                    fileid = ?
            WHERE eventid = ?
                AND userid = ?;
            """
        self.cursor.execute(sql,(grade,message,fileID,eventID,userID))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output


    def getAllGradesPlusNamesWithEventID(self,eventID):
        sql = """
            SELECT 
                u.firstname,
                u.lastname,
                g.grade,
                g.message,
                g.fileid,
                g.userid
            FROM grade AS g
            INNER JOIN user AS u
                ON g.userid = u.userid
            WHERE g.eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
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
            WHERE ex.courseid = ?
            ORDER BY ev.date ASC;
            """
        self.cursor.execute(sql,(userID, courseID))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output


    def deleteAllGradesWithEventID(self,eventID):
        sql= """
            DELETE FROM grade
            WHERE eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        self.conn.commit()
        return 
    






class Exam:

    conn = None
    cursor = None

    def __init__(self):
        return

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



    def addNewExamen(self,courseID, eventID, testName,weight):
        sql = "INSERT INTO examen (courseid,eventid,testname,weight,changedatum) VALUES (?,?,?,?, DATETIME('now'))"
        self.cursor.execute(sql, (courseID,eventID,testName,weight))
        self.conn.commit()
        return True


    def getAllExamsFromCourseID(self,courseID):
        sql = """SELECT 
        ex.testname, 
        ex.weight,
        ev.date,
        ex.eventid
        FROM examen AS ex
        INNER JOIN event AS ev
            ON ex.eventid = ev.eventid
        WHERE ex.courseid = ?
        ORDER BY ev.date ASC;
        """
        self.cursor.execute(sql, (courseID,))
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
                ev.describtion,
                ex.courseid,
                ex.eventid
            FROM examen AS ex
            INNER JOIN event AS ev
                ON ex.eventid = ev.eventid
            WHERE ex.eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        output = self.cursor.fetchall()
        self.conn.commit()
        return output[0]


    def updateAllExamAndEventDataWithEventID(self,testName,weight,location,date,starttime,endtime,description,courseID,eventID):
        sql = """
            UPDATE examen
                SET testname = ?,
                    weight = ?
                WHERE eventid = ? 
            """
        self.cursor.execute(sql,(testName,weight,eventID))
        self.conn.commit()
        sql = """
            UPDATE event
                SET location = ?,
                    date = ?,
                    starttime = ?,
                    endtime = ?,
                    describtion = ?

                WHERE eventid = ? 
            """
        self.cursor.execute(sql,(location,date,starttime,endtime,description,eventID))
        self.conn.commit()
        return


    def deleteExamWithEventID(self,eventID):
        sql= """
            DELETE FROM examen
            WHERE eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        self.conn.commit()
        return 






class Event:

    conn = None
    cursor = None

    def __init__(self):
        return  
    
    
    def isUserIDinEvent(self,userID, eventID):
        sql = """
            SELECT EXISTS(
                SELECT 1
                FROM event
                INNER JOIN course
                    ON course.courseid = event.courseid
                WHERE userid = ?
                    AND eventid = ?
            );
            """
        self.cursor.execute(sql, (userID,eventID))
        self.conn.commit()
        return True


    def deleteEventWithEventID(self,eventID):
        sql= """
            DELETE FROM event
            WHERE eventid = ?;
            """
        self.cursor.execute(sql,(eventID,))
        self.conn.commit()
        return 

    


class Course:

    conn = None
    cursor = None

    def __init__(self):
        return  




class Database(FcmToken,User,File,Token,Grade,Exam,Event,Course):

    conn = None
    cursor = None

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()




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
    

    def creatTableEvent(self):
        self.cursor.execute("DROP TABLE IF EXISTS event")
        tableCreationQuery = """
        CREATE TABLE event (
            eventid TEXT NOT NULL,
            location TEXT NOT NULL,
            date TEXT NOT NULL,
            starttime TEXT NOT NULL,
            endtime TEXT NOT NULL,
            courseID TEXT NOT NULL,
            describtion TEXT,
            type INT            
        );
        """

        # type Exam = 666
        self.cursor.execute(tableCreationQuery)
        self.conn.commit()
        return True




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


    def addNewCourse(self,courseID,userID,subject,courseName):
        sql = "INSERT INTO course (courseid,userid,subject,courseName) VALUES (?,?,?,?)"
        self.cursor.execute(sql, (courseID,userID,subject,courseName))
        self.conn.commit()
        return True


    def addNewEvent(self,eventID,location,date,starttime,endtime,describtion,kind,courseID):
        sql = "INSERT INTO event (eventid, location, date, starttime, endtime, describtion, type,courseid) VALUES (?,?,?,?,?,?,?,?)"
        self.cursor.execute(sql, (eventID,location,date, starttime, endtime, describtion, kind,courseID))
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








    def getALLCourseWithUserID(self,userID):
        sql = "SELECT courseid,subject,courseName FROM course WHERE userid = ?"
        self.cursor.execute(sql, (userID,))
        output = self.cursor.fetchall()
        self.conn.commit()

        return output


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


