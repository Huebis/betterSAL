import { Injectable } from '@angular/core';
import { PushNotifications, Token} from '@capacitor/push-notifications';
import { ApiService } from './api';
import { PushNotificationAlertComponent } from '../alerts/push-notification-alert/push-notification-alert.component';

@Injectable({
  providedIn: 'root',
})
export class PushNotification {
  constructor(
    private api: ApiService){
    this.initPushNotifications();
  }
  hardwareID="test";
  
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
      this.registerFcmToken(token);
    });
    
    PushNotifications.addListener('pushNotificationReceived', async (notification) => {
      console.log('Push Notification received in foreground:', notification);
      //await this.showAlert(notification);
      //await this.showLocalNotification(notification.title ?? 'Neue Nachricht', notification.body ?? '').then();
      });

    PushNotifications.addListener('registrationError', (error) => {
      console.error('Registration error:', error);
    });
  }

  registerFcmToken(token:any){

    this.api.sendRequestPost({fcmToken:token.value, hardwareID: this.hardwareID},"postFcmToken").subscribe( v => {
      console.log(v);
    });
  }

}
