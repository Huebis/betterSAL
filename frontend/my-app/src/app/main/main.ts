import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

import { AuthService } from '../auth';

import { NavbarComponent } from '../navbar/navbar';



@Component({
  selector: 'app-main',
  imports: [RouterOutlet, NavbarComponent],
  templateUrl: './main.html',
  styleUrl: './main.css',
})
export class MainComponent {


}
