import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MenuComponent } from './menu/menu';
import { TimetableComponent } from './timetable/timetable';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, MenuComponent, TimetableComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('my-app');
}
