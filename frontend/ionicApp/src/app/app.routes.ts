import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

import { LoginPage } from './page/loginpage/loginpage.component';
import { HomePage } from './page/home/home.page';
import { GradesComponent } from './component/grades/grades.component';

export const routes: Routes = [
  { path: 'home', 
    component:HomePage,
    children:[
      {path:'grades',component:GradesComponent},
    ]
  },
  { path: 'login', component:LoginPage},
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
];

@NgModule({
  imports: [
      RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
