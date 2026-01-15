import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../auth';

import { ApiService } from '../api.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
})
export class LoginComponent {
  username = '';
  password = '';
  uuid='';

  constructor(private authService: AuthService, private router: Router, private api: ApiService) {}

  login() {
    //let data="{'username:'{$this.username}','password':'{$this.password}'}"
    let data={username:"Eliah",password:"Eliah"}
    let senddata = JSON.stringify(data);

    this.api.sendRequest(senddata,"login").subscribe({
      next: res => console.log(res),
      error: err => console.error('HTTP Error:', err)
    });

    console.log(this.uuid)
    const value = this.uuid.trim();
    if (!value) {
      alert('UUID is required');
      return;
    }

    this.authService.setUuid(value);
    this.router.navigateByUrl('/dashboard');
  }
}
