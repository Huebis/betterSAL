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

### register
/register_user

#### input
username (plain, json)
password (plain, json)
email (plain, json)

#### output


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

### getfile
/get_file_by_id

#### input
token
fileId (json)

#### output
file (attachment)

### getGradesStudent
/get_grades_student
#### input
token
#### output
subjects:{{name, grade, date, message, fileId},...} (json) 


### addNewTest
/addNewTest
#### input
token
courseID, testName, weight, location, date, starttime, endtime, describtion


### getTest
/get_test_by_id
#### input
token
testId (json)
#### output
{name, date, students:{{studentName, grade, message, fileId},...}} (json) 

### postTest
/post_test_by_id
#### input
token
{testId,students:{{studentName, grade, message, fileId},...}} (json)


### getAllTests
/get_tests
#### input
token
#### output
{{courseId, subject, tests,{{testId, name, date, greaded},...}}...} (json)




## ERRORS

| ERROR number| Description |
| ----------- | ----------- |
| 200         | OK          |
| 403         | token invalid|
