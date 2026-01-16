import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { UserMenuComponent } from './user-menu/user-menu';
import { TimetableComponent } from './timetable/timetable';
import { LoginpageComponent } from './loginpage/loginpage';
import { RegisterComponent } from './register/register';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})


export class App {
  protected readonly title = signal('my-app');
}
