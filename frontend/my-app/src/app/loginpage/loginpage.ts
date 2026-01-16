import { Component, input, ViewChild, AfterViewInit} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { PasswordComponent} from '../passwordinput/passwordinput';
import { AuthService } from '../auth';
import { ApiService } from '../api.service';


@Component({
  selector: 'app-loginpage',
  imports: [PasswordComponent, CommonModule, FormsModule],
  templateUrl: './loginpage.html',
  styleUrl: './loginpage.css',
})
export class LoginpageComponent {
  username = '';
  
  constructor(private authService: AuthService, private router: Router, private api: ApiService) {}

  @ViewChild(PasswordComponent) passwordComponent!: PasswordComponent;

  login() {
    
    let data={
      username:this.username,
      password:this.passwordComponent.password
    }
    this.api.sendRequest(data,"login").subscribe({
      next: res => {
        this.authService.setUuid(res["token"]);
        console.log("loged in")
      },
      error: err => console.error('HTTP Error:', err)
    });   
  }

}
