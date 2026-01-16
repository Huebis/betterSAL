import { Component, input, ViewChild, AfterViewInit} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { PasswordComponent} from '../passwordinput/passwordinput';
import { AuthService } from '../auth';
import { ApiService } from '../api.service';



@Component({
  selector: 'app-register',
  imports: [PasswordComponent, CommonModule, FormsModule],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class RegisterComponent {
  username = '';
  email = '';


  constructor(private router: Router, private authService: AuthService, private api: ApiService) {}

  @ViewChild(PasswordComponent) passwordComponent!: PasswordComponent;

  register() {
    let data={
      username:this.username,
      password:this.passwordComponent.password,
      email:this.email
    }
    this.api.sendRequest(data,"register_user").subscribe({
      next: res => {
        this.authService.setUuid(res["token"]);
        console.log("registered");

        this.router.navigate(['/main'])

      },
      error: err => console.error('HTTP Error:', err)
    });   
  }
}
