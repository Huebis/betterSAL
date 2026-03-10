import { Injectable } from '@angular/core';
import { AlertController } from '@ionic/angular';
import { PushNotifications, Token} from '@capacitor/push-notifications';
import { ApiService } from './api';

@Injectable({
  providedIn: 'root',
})
export class PushNotification {
  constructor(private api: ApiService, private alertController: AlertController){
    this.initPushNotifications();
  }

  
  initPushNotifications() {
    PushNotifications.requestPermissions().then(result => {
      if (result.receive === 'granted') {
        this.registerForPushNotifications();
      } else {
        console.error('Notification permission denied');
      }
    });
  }

  registerForPushNotifications() {
    console.log('Registering for push notifications...');
    PushNotifications.register();

    PushNotifications.addListener('registration', (token:Token) => {
      this.api.sendRequestPost({fcmToken:token.value},"testFcmToken").subscribe( v => {
        console.log(v);
      });
    });
    
    PushNotifications.addListener('pushNotificationReceived', async (notification) => {
      console.log('Push Notification received in foreground:', notification);
      await this.showLocalNotification(notification.title ?? 'Neue Nachricht', notification.body ?? '').then();
      });

    PushNotifications.addListener('registrationError', (error) => {
      console.error('Registration error:', error);
    });
  }

  async showLocalNotification(title: string, message: string) {
    const alert = await this.alertController.create({
      cssClass: 'my-custom-class',
      header: 'Confirm!',
      message: 'Message <strong>text</strong>!!!',
      buttons: [
        {
          text: 'Cancel',
          role: 'cancel',
          cssClass: 'secondary',
          handler: (blah) => {
            console.log('Confirm Cancel: blah');
          }
        }, {
          text: 'Okay',
          handler: () => {
            console.log('Confirm Okay');
          }
        }
      ]
    });

    await alert.present();
  }

}
