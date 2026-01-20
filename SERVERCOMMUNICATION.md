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

### register
/register_user

#### input
username (plain, json)
password (plain, json)
email (plain, json)

#### output


### endSession
/endSession

#### input
token (plain, json)

#### output
empty Json

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
subjects:[{name,[{ grade, date, message, fileId},...]},...](json) 


### createTest
/create_test
#### input
token
course, testName, date, startTime, endTime, weight (json)


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


### getTests
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
