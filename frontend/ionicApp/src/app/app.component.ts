import { Component } from '@angular/core';
import { IonApp, IonRouterOutlet, IonMenu, IonContent, IonButton } from '@ionic/angular/standalone';
import { MenusComponent } from "./menus/menus.component";
import { Platform } from '@ionic/angular';
import { PushNotification } from './service/push-notification'

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  imports: [IonApp, IonRouterOutlet, MenusComponent],
})
export class AppComponent {
  constructor(
    private platform: Platform,
    private pushNotification: PushNotification) {
    console.log("------------------------");
    this.platform.ready().then(() => {
      // Push notifications will be initialized on service instantiation
    });
  }
}
