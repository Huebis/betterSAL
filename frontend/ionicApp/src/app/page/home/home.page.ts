import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { IonHeader, IonToolbar, IonContent, IonItem, IonButton } from '@ionic/angular/standalone';

import { UserSmallComponent } from '../../component/user-small/user-small.component';
import { PushNotification } from 'src/app/service/push-notification';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonHeader, IonToolbar, IonContent, IonItem, UserSmallComponent, RouterOutlet, IonButton],
})
export class HomePage{
  constructor(private router: Router, private pushNotification: PushNotification) {}

  
  navigateTo(substing:string){
    this.router.navigate([substing]);
  }
  sendNoti(){
    this.pushNotification.showLocalNotification("test","test").then();
  }

}

