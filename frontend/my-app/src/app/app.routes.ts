import { Routes } from '@angular/router';
import { LoginComponent } from './login/login';
import { MenuComponent } from './menu/menu';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: MenuComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' }
];
