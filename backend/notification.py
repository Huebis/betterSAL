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
    token="f5KVjRZUQB-iboK7KakJet:APA91bFassSDzVBJbfmSq14v6VWDAg8VpfbmsFLGjs5p5w4Mm--zeWVhJ2Sq2v1t75Hg73SnFVIjoPQ5AK0gQ87dNfCUM-oyO-0DtrBMXhQv0ZM4-h6j6Is",
    title="Unterricht!",
    body="Die Stunde geht noch 10 Minuten "
))

