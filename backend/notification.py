import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("bettersal-firebase-adminsdk-fbsvc-75263d9492.json")
firebase_admin.initialize_app(cred)


def send_push(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token,
    )

    response = messaging.send(message)
    return response


print(send_push(
    token="dhfSI4esQ1GDL2nFUYIpwb:APA91bHqYNwaI2ezidpjDdyT6bOKAHLPZsBbwbtYadkHeyBtM9fP0Jxnyy0NZcJtddVjguOVwFVYyCD1Be9-UR1CptuNkoPOor1Gq01xEoMRsk-5Le8aPzA",
    title="Hallo!",
    body="Das ist eine Push-Nachricht"
))

