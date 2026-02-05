import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

import { IonItem, IonInput, IonIcon, IonButton, IonInputPasswordToggle} from '@ionic/angular/standalone';

import { AuthService } from '../../service/auth';
import { ApiService } from '../../service/api';

@Component({
  selector: 'app-loginpage',
  templateUrl: './loginpage.component.html',
  styleUrls: ['./loginpage.component.scss'],
  imports: [FormsModule, IonItem, IonInput, IonButton, IonInputPasswordToggle]
})
export class LoginPage  implements OnInit {
  ngOnInit() {}
  username="";
  password="";

  constructor(private authService: AuthService, private router: Router, private api: ApiService) {}

  login(){
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
        this.router.navigate(['/home'])
      },
      error: err => console.error('HTTP Error:', err)
    }); 

  }

}
