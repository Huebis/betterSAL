import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { IonHeader, IonToolbar, IonContent, IonItem, IonButton, IonList } from '@ionic/angular/standalone';

import { PushNotification } from 'src/app/service/push-notification';
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";
import { FileDownloadComponent } from "src/app/component/file-download/file-download.component";
import { UserSmallComponent } from "src/app/component/user-small/user-small.component";

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonList, IonHeader, IonToolbar, IonContent, IonItem, RouterOutlet, IonButton, FileUploadComponent, FileDownloadComponent, UserSmallComponent],
})
export class HomePage{
  constructor(private router: Router, private pushNotification: PushNotification) {}

  
  navigateTo(substing:string){
    this.router.navigate([substing]);
  }
  sendNoti(){
    this.pushNotification.showNotification({test:"test"});
    //this.pushNotification.showAlert("test").then();
  }

}

