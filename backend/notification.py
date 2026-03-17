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
    # 5 = notifgradechange
    permissions = db.getNotificationPermissionsOfUser(userID)

    if notificationType < 0 or notificationType > 6:
        raise ExceptionType("Wrong notificationType !!!!!!!, fix pleas")

    
    if notificationType != 6: # 5 ist für Sudo
        if permissions[notificationType] != 1:
            return 

    


    #list of fcmToken (but tuple)
    AllFcmToken = db.getAllFcmTokenFromUserID(userID)

    for fcmToken in AllFcmToken:
        try:
            sendNotification(fcmToken[0],title,body)
            print("hat gesendet")
        except:
            #wenn ein FCM-Token nicht funktioniert bzw. Error kommt,  FCM-Token löschen
            print("FCM TOKEN MUSSTE gelöscht werden, da er nicht gestummen hat ")
            db.deleteFcmTokenWithUserIDAndFcmToken(userID,fcmToken[0])

    return 








#sentNotificationToUserID("de","","test","test",1)
"""
print(sendPush(
    token="dzxVSBmWTWKaOiqd23iq04:APA91bHcg4A9f94IcXAjG_59N9Nt0Eq5LQty_0pT2muoUueqy3y0ESrTGJH95NjAdDb2A1BL4AHf3CU8FtBtNURWxlJrpesisaNwfJQdy6g_XIopM8gHVjE",
    title="Hallo Theo!",
    body="Du wurdest gehacked"
))

"""