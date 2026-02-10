import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("bettersal-firebase-adminsdk-fbsvc-06bd88d65c.json")
firebase_admin.initialize_app(cred)


def sendPush(token, title, body):
    message = messaging.Message(    
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data={
            "title": title,
            "body": body
        },
        token=token,
    )

    response = messaging.send(message)
    return response



print(sendPush(
    token="dzxVSBmWTWKaOiqd23iq04:APA91bHcg4A9f94IcXAjG_59N9Nt0Eq5LQty_0pT2muoUueqy3y0ESrTGJH95NjAdDb2A1BL4AHf3CU8FtBtNURWxlJrpesisaNwfJQdy6g_XIopM8gHVjE",
    title="Hallo!",
    body="Das ist eine Push-Nachricht"
))

