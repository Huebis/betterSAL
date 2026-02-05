import { AfterViewInit, Component, OnInit } from '@angular/core';

import { IonButton, IonAvatar, IonMenu, IonContent } from "@ionic/angular/standalone";
import { MenuController } from '@ionic/angular'; //import MenuController to access toggle() method.



@Component({
  selector: 'app-menus',
  templateUrl: './menus.component.html',
  styleUrls: ['./menus.component.scss'],
  imports:[IonButton, IonMenu, IonContent]
})
export class MenusComponent{

  constructor(private menuCtrl: MenuController) {
    this.menuCtrl.enable(true);
   }

  ionViewDidEnter() { 
    this.openMenu("user");
  }
  openMenu(menuId:string){
    this.menuCtrl.open(menuId).then();
    console.log(menuId+" opened");
  }
  closeMenu(menuId:string){
    this.menuCtrl.getOpen().then(v => console.log(v)).catch(v => console.log(v));
    this.menuCtrl.close();
    this.menuCtrl.isOpen("user").then(v => console.log(v));
  }

}
