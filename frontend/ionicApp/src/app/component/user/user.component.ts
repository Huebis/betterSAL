import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


import { IonButton } from "@ionic/angular/standalone";

import { AuthService } from '../../service/auth';
import { ApiService } from '../../service/api';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
  imports: [IonButton],
})
export class UserComponent  implements OnInit {

  constructor(private authService: AuthService, private router: Router, private api: ApiService) {}

  ngOnInit() {}
  logout(){
    this.api.sendRequest({},"endSession").subscribe({
      next: res => {
        this.authService.clearUuid();
        console.log("loged out")
        this.router.navigate(['/home'])
      },
      error: err => {console.error('HTTP Error:', err)}
    }); 
  };
  navigateTo(substing:string){
    this.router.navigate([substing]);
  }
  isLoggedIn(){
    return this.authService.isLoggedIn();
  }
}
