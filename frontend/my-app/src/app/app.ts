import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MenuComponent } from './menu/menu';
import { TimetableComponent } from './timetable/timetable';
import { Loginpage } from './loginpage/loginpage';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MenuComponent, TimetableComponent, Loginpage],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('my-app');
}
