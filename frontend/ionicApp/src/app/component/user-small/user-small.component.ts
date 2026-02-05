import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { MenuController } from '@ionic/angular';
import { IonAvatar } from "@ionic/angular/standalone";

import { AuthService } from '../../service/auth';
import { ApiService } from '../../service/api';

@Component({
  selector: 'app-user-small',
  templateUrl: './user-small.component.html',
  styleUrls: ['./user-small.component.scss'],
  imports: [IonAvatar]
})
export class UserSmallComponent  implements OnInit {
  constructor(private authService: AuthService, private router: Router, private api: ApiService, private menu: MenuController) {}

  ngOnInit() {}
  logout(){
    this.api.sendRequestPost({},"endSession").subscribe({
      next: res => {
        this.authService.clearUuid();
        console.log("loged out")
        this.menu.close("user");
      },
      error: err => {console.error('HTTP Error:', err)}
    }); 
  };
  navigateTo(substing:string){
    this.router.navigate([substing]);
    this.menu.close("user");
  }
  isLoggedIn(){
    return this.authService.isLoggedIn();
  }
  openMenu(){
    this.menu.open("user").then(()=>{
      console.log("opend");
    }).catch((error) => {
      console.error('Error opening menu: ', error);
    });
  }
  closeMenu(){
    this.menu.close("user");
  }

}
