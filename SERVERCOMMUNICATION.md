# Server comunication


## Endpoints
Comunication in JSON format
### /register_user
Input: {"username":"","password":""}

Ouput: {}

### /login
Input: {"username":"","password":""}

Ouput: {"nickname":""}

## ERRROR
Each output also contains a {"EROOR":"0"}

| ERROR number| Description |
| ----------- | ----------- |
| 0           | No Error    |
| 1           | A Error     |
| 2           | Missing Data|
| 10          | Username already exists|
