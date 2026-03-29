import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import {IonInput, IonButton, IonInputPasswordToggle, IonContent } from '@ionic/angular/standalone';

import { AuthService } from '../../service/auth';
import { ApiService } from '../../service/api';
import { PushNotification } from 'src/app/service/push-notification';

@Component({
  selector: 'app-loginpage',
  templateUrl: './loginpage.component.html',
  styleUrls: ['./loginpage.component.scss'],
  imports: [FormsModule, IonInput, IonButton, IonInputPasswordToggle, IonContent]
})
export class LoginPage  implements OnInit {
  ngOnInit() {
    this.message="";
  }
  username="";
  password="";
  message="";

  constructor(
    private authService: AuthService, 
    private router: Router, 
    private api: ApiService,
    private notifications: PushNotification) {}

  login(){
    this.message="loading";
    console.log(this.username)
    let data={
      username:this.username,
      password:this.password
    }
    this.api.sendRequestPost(data,"login").subscribe({
      next: res => {
        this.authService.setUuid(res["token"]);
        this.authService.setRole(res["role"]);
        this.username="";
        this.password="";
        this.router.navigate(['/home']);
        this.notifications.initPushNotifications();

      },
      error: err => {
        console.log(err.error.error);
        if (err.error.error==="username and password are wrong"){
          this.message="username or password is wrong";
        }else{
          this.message="networking error";
        }
        console.error('HTTP Error:', JSON.stringify(err));

      }
      
    }); 

  }

}
