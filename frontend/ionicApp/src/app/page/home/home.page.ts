import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { IonHeader, IonToolbar, IonContent, IonItem} from '@ionic/angular/standalone';

import { UserSmallComponent } from '../../component/user-small/user-small.component';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonHeader, IonToolbar, IonContent, IonItem, UserSmallComponent, RouterOutlet],
})
export class HomePage {
  constructor(private router: Router) {}
  navigateTo(substing:string){
    this.router.navigate([substing]);
  }
}
