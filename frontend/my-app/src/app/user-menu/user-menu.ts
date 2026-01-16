import { Component } from '@angular/core';

import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { AuthService } from '../auth';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-user-menu',
  imports: [],
  templateUrl: './user-menu.html',
  styleUrl: './user-menu.css',
})
export class UserMenuComponent {
  constructor(private authService: AuthService, private router: Router, private api: ApiService) {};

  logout(){
    this.api.sendRequest({},"endSession").subscribe({
      next: res => {
        this.authService.clearUuid();
        console.log("loged out")
        this.router.navigate(['/main'])
      },
      error: err => console.error('HTTP Error:', err)
    }); 
  }
}
