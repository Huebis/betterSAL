import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Router } from '@angular/router';

import { AuthService } from '../auth';
import { UserMenuComponent } from '../user-menu/user-menu';


@Component({
  selector: 'app-main',
  imports: [RouterOutlet, UserMenuComponent],
  templateUrl: './main.html',
  styleUrl: './main.css',
})
export class MainComponent {
  uuid:string|null=null;
  constructor(private router: Router,private authService: AuthService) {
    if (this.authService.isLoggedIn()){
      this.uuid=this.authService.getUuid();
    }else{
      this.uuid="logged out";
    }}

  navigateTo(path:string){
    this.router.navigate([path])
  }

  

}
