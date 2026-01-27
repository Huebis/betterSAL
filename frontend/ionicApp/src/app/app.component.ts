import { Component } from '@angular/core';
import { IonApp, IonRouterOutlet, IonMenu, IonContent, IonButton } from '@ionic/angular/standalone';
import { MenusComponent } from "./menus/menus.component";

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  imports: [IonApp, IonRouterOutlet, MenusComponent],
})
export class AppComponent {
  constructor() {}
}
