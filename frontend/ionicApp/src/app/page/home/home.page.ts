import { Component, OnInit } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

import { IonHeader, IonToolbar, IonContent, IonItem, IonButton, IonList } from '@ionic/angular/standalone';

import { UserSmallComponent} from '../../component/user-small/user-small.component';
import { FileInputComponent } from 'src/app/component/fileinput/fileinput.component';
import { PushNotification } from 'src/app/service/push-notification';
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";
import { FileDownloadComponent } from "src/app/component/file-download/file-download.component";

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  imports: [IonList, FileInputComponent, IonHeader, IonToolbar, IonContent, IonItem, UserSmallComponent, RouterOutlet, IonButton, FileUploadComponent, FileDownloadComponent],
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

