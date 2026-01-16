import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main',
  imports: [RouterOutlet],
  templateUrl: './main.html',
  styleUrl: './main.css',
})
export class MainComponent {
  constructor(private router: Router) {}
  navigateTo(path:string){
    this.router.navigate([path])
  }

}
