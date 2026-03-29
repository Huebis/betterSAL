import { Injectable } from '@angular/core';
import { PushNotifications, Token} from '@capacitor/push-notifications';
import { ApiService } from './api';
import { Toast } from '@capacitor/toast'
import { AuthService } from './auth';

@Injectable({
  providedIn: 'root',
})
export class PushNotification {
  constructor(
    private api: ApiService,
    private auth: AuthService){
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
        this.showNotification(notification);
      });

    PushNotifications.addListener('registrationError', (error) => {
      console.error('Registration error:', error);
    });
  }

  registerFcmToken(token:any){
    this.api.sendRequestPost({fcmToken:token.value},"postFcmToken").subscribe();
  }

  showNotification = async (notification:any) => {
    await Toast.show({
      text: notification.data.body,
      position: 'top',
    })
  }

}
