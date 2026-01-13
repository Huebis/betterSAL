import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './login.html'
})
export class Login {
  uuid = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  login(): void {
    const value = this.uuid.trim();

    if (!value) {
      alert('UUID is required');
      return;
    }

    // Optional: UUID format validation
    const uuidRegex =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

    if (!uuidRegex.test(value)) {
      alert('Invalid UUID format');
      return;
    }

    this.authService.setUuid(value);
    this.router.navigateByUrl('/');
  }
}
