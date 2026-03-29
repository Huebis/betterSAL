# Server comunication

## Interfaces
/betterSAL/api ...

### Login
/login
#### input
username (plain, json)
password (plain, json)
#### output
token
role

### password Change
/changePassword

#### input
token (plain, json)
password (plain, json)
newPassword (plain, json)

#### output
empty JSON



### endSession
/endSession

#### input
token (plain, json)

#### output
empty JSON



### getGradesStudent
/getGradesStudent

#### input
token

#### output
subjects (array)


### addNewTest
/addNewTest
#### input
token
courseID
testName
weight
location
date
starttime
endtime
description

#### output
empty JSON


### deleteTest
/deleteTest
#### Input
token
eventID
#### output
empty JSON


### getAllTests
/getAllTests
#### Input
token
#### output
courses


### getAllGradesFromTest
/getAllGradesFromTest
#### Input
token
eventID (url Parameter)
courseID (url Parameter)
#### output 
grades
exam


### postAllGradesFromAllStudentsOfTest
/postAllGradesFromAllStudentsOfTest
Es ist die Inverse Funktion von getAllGradesFromTest, die genau gleichen Daten können (verändert) wieder zurück geschickt werden
#### Input
token
grades
exam
#### output
empty JSON



### getUserData
/getUserData
#### Input
token
#### output
userName
ClassName
major
email
role
firstName
lastName
notifAbsenceOfTeacherToday
notifAbsenceOfTeacherTomorrow
notifExamTomorrow
notifEventTomorrow
notifAbsenceDueTomorrow
notifGradeChange




### postAllUserInformation
/postAllUserInformation
Inversion von getUserData, Objekt kann (verändert) einfach wieder zurück geschickt werden.
#### Input
token
userName
email
notifAbsenceOfTeacherToday
notifAbsenceOfTeacherTomorrow
notifExamTomorrow
notifEventTomorrow
notifAbsenceDueTomorrow
notifGradeChange
#### output
courses


### getSchedule
/getSchedule
#### Input
token
starttime (url Parameter)
endtime (url Parameter)
#### output
schedule


### changeAndMergeAbsence
/absence
#### Input
token
requestType (url Parameter) "merge" / "change"

bei merge: absenceIDList
bei change: absenceID, excused, description,fileID
#### output
empty JSON


### getAbsence
/absence
#### Input
token
#### output
absence

### deleteAbsenceEvent
/absence
#### Input
token
userID
eventID
absenceID
#### output
empty JSON


### getAnwesenheitsliste
/presenceList
#### Input
token
starttime (url Parameter)
endtime (url Parameter)
eventID (url Parameter)
courseID (url Parameter)
#### output
anwesenheitsliste
lesson

### postAnwesenheitsliste
/presenceList
Inversionsfunktion von getAnwesenheitsliste, gleiche Daten (verändert) wieder zurückschicken.
#### Input
token
anwesenheitsliste
lesson
#### output
empty JSON

### uploadFile
/file
#### Input
token
file
#### output
fileID

### download_file
//file/<fileID>
#### Input
token
<fileID> (in url)
#### output
file

### addEvent
/addEvent
#### Input
token
courseID
type
description
fileID
starttime
endtime
location

#### output
empty JSON

### getCourses
/getCourses
#### Input
token
#### output
courses

### getAbsence
/absence
#### Input
token
#### output
absence

### Output

## ERRORS

| ERROR number| Description |
| ----------- | ----------- |
| 200         | OK          |
| 400         | API-Input is invalid or backend prozess failed|
| 450         | token invalid|



