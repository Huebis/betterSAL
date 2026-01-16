import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MenuComponent } from './menu/menu';
import { UserMenuComponent } from './user-menu/user-menu';
import { TimetableComponent } from './timetable/timetable';
import { LoginpageComponent } from './loginpage/loginpage';
import { ApiService } from './api.service';

@Component({
  selector: 'app-root',
  imports: [MenuComponent, LoginpageComponent, UserMenuComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('my-app');
}
