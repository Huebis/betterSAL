import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <h2>Login</h2>
    <input type="text" placeholder="Enter UUID" [(ngModel)]="uuid"/>
    <button (click)="login()">Login</button>
  `
})
export class LoginComponent {
  uuid = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    const value = this.uuid.trim();
    if (!value) {
      alert('UUID is required');
      return;
    }

    this.authService.setUuid(value);
    this.router.navigateByUrl('/dashboard');
  }
}
