import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import {CanMatchGuard} from './service/can-match-guard'

import { LoginPage } from './page/loginpage/loginpage.component';
import { HomePage } from './page/home/home.page';
import { GradesComponent } from './component/grades/grades.component';
import { TeacherGradesComponent } from './component/teacher-grades/teacher-grades.component';
import { ChangeExamComponent } from './component/change-exam/change-exam.component';
import { AbsencesComponent } from './component/absences/absences.component';


export const routes: Routes = [
  { path: 'home', 
    component:HomePage,
    children:[
      {path:'grades',component:TeacherGradesComponent, canMatch: [CanMatchGuard],data:{allowedRoles:[false,false,true,false,false]}},
      {path:'grades',component:GradesComponent},
      {path:'changeExam/:courseID/:eventID',component:ChangeExamComponent},

      {path:'absences',component:AbsencesComponent}
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
