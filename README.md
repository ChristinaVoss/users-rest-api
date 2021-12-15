# users-rest-api
Simple REST API for creation, reading and deletion of users.

## Setup
To initialise and run this code, run the following in the terminal

```
// MAC & UNIX:
export FLASK_APP=app.py

// WINDOWS:
set FLASK_APP=app.py

flask db init
flask db migrate -m "first migration"
flask db upgrade
python app.py
```

## Testing with curl (examples)
*Note: use actual examples of names/emails/passwords rather than the <name> etc placeholders. If there are quotation marks surrounding the placeholder, use them in the real request as well.*

GET ALL
```
curl http://127.0.0.1:5000/users
```
GET 1
```
curl http://127.0.0.1:5000/user/<name>
```
POST
```
curl -X POST http://127.0.0.1:5000/user/<name>/<email>/<password>
```
AUTHENTICATE user to get access token (for deletion):
```
curl -H "Content-Type: application/json" -X POST   -d '{"username":"<name>","password":"<password>"}' http://127.0.0.1:5000/auth
// this returns a token - copy including quotation marks

// then export the provided token:
export ACCESS="<token>"

// then finally use this exported token in the delete request:
curl -H "Authorization: JWT $ACCESS" -X DELETE http://127.0.0.1:5000/user/<email>
```
