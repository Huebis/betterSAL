import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-navbar',
  imports: [],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class NavbarComponent {
  constructor(private router: Router) {};

  changePage(page:string){
    this.router.navigate(["main/"+page]);
  }
}
