import { Component } from '@angular/core';

@Component({
  selector: 'app-passwordinput',
  imports: [],
  templateUrl: './passwordinput.html',
  styleUrl: './passwordinput.css',
})
export class Passwordinput {
  password: string = '';
  showPassword: boolean = false;
  togglePasswordVisibility(): void {
    this.showPassword = !this.showPassword;
  }

}
