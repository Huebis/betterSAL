import { Routes } from '@angular/router';
import { LoginpageComponent } from './loginpage/loginpage';
import { RegisterComponent } from './register/register';
import { MainComponent } from './main/main';

import { UserMenuComponent } from './user-menu/user-menu';


export const routes: Routes = [
  { path: 'login', component:LoginpageComponent},
  { path: 'register', component:RegisterComponent},
  { path: 'main',
    component:MainComponent,
    children:[
      {path:'user',component:UserMenuComponent}
    ]
  },
  { path: '*', redirectTo:'main'}
];
