import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("bettersal-firebase-adminsdk-fbsvc-06bd88d65c.json")
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
    token="cILTay5eTjqXdmPXAdUOAX:APA91bEpvN--ge2PxGmR9CLumZNi09kZrtHTzuZ33rgDq76CeqMIwzBinAaWiN8LC3ce-eNH5HsLWrqMbPS7z3z2wEm1IiE8KjCVdSLNea0MRm52KQ4OUEc",
    title="Hallo!",
    body="Das ist eine Push-Nachricht"
))

