import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-passwordinput',
  imports: [FormsModule],
  templateUrl: './passwordinput.html',
  styleUrl: './passwordinput.css',
})
export class PasswordComponent {
  password: string = '';
  showPassword: boolean = false;
  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }
}
