import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MenuComponent } from './menu/menu';
import { TimetableComponent } from './timetable/timetable';
import { Loginpage } from './loginpage/loginpage';
import { Login } from './login/login';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  imports: [Login, MenuComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('my-app');
}
