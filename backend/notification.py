import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("bettersal-firebase-adminsdk-fbsvc-06bd88d65c.json")
firebase_admin.initialize_app(cred)



def sendNotification(token, title, body):
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







def sentNotificationToUserID(db,userID,title,body,notificationType):
    #Permission von user für notificationType abfragen.

    # 0 = notifabsenceofteachertoday
    # 1= notifabsenceofteachertomorrow
    # 2= notifexamtomorrow
    # 3= notifeventtomorrow
    # 4= notifabsenceduetomorrow
    permissions = db.getNotificationPermissionsOfUser(userID)

    if notificationType < 0 or notificationType > 5:
        raise ExceptionType("Wrong notificationType !!!!!!!, fix pleas")

    
    if notificationType != 5: # 5 ist für Sudo
        if permissions[notificationType] != 1:
            return 

    



    AllFcmTokenWithHardwareID = db.getAllFcmTokenFromUserID(userID)

    for fcmTokenPair in AllFcmTokenWithHardwareID:
        try:
            sendNotification(fcmTokenPair[0],title,body)
        except:
            #wenn ein FCM-Token nicht funktioniert bzw. Error kommt,  FCM-Token löschen
            print("FCM TOKEN MUSSTE gelöscht werden, da er nicht gestummen hat ")
            db.deleteFcmTokenWithUserIDAndHardwareID(userID,fcmTokenPair[1])

    return 








#sentNotificationToUserID("de","","test","test",1)
"""
print(sendPush(
    token="dzxVSBmWTWKaOiqd23iq04:APA91bHcg4A9f94IcXAjG_59N9Nt0Eq5LQty_0pT2muoUueqy3y0ESrTGJH95NjAdDb2A1BL4AHf3CU8FtBtNURWxlJrpesisaNwfJQdy6g_XIopM8gHVjE",
    title="Hallo Theo!",
    body="Du wurdest gehacked"
))

"""