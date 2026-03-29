import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import {CanMatchGuard} from './service/can-match-guard'

import { LoginPage } from './page/loginpage/loginpage.component';
import { HomePage } from './page/home/home.page';
import { GradesSubpage } from './subpages/grades/grades.subpage';
import { TeacherGradesSubpage } from './subpages/teacher-grades/teacher-grades.subpage';
import { ChangeExamSubpage } from './subpages/change-exam/change-exam.subpage';
import { AbsencesSubpage } from './subpages/absences/absences.subpage';
import { TimetableSubpage } from './subpages/timetable/timetable.subpage';
import { CheckPresenseSubpage } from './subpages/check-presense/check-presense.subpage';
import { UserComponent } from './subpages/user/user.component';
import { TeacherAbsencesSubpage } from './subpages/teacher-absences/teacher-absences.subpage';
import { EventComponent } from './subpages/event/event.component';


export const routes: Routes = [
  { path: 'home', 
    component:HomePage,
    children:[
      {path:'grades',component:TeacherGradesSubpage, canMatch: [CanMatchGuard],data:{allowedRoles:[false,false,true,false,false]}},
      {path:'grades',component:GradesSubpage},
      {path:'changeExam/:courseID/:eventID',component:ChangeExamSubpage},

      {path:'absences',component:TeacherAbsencesSubpage, canMatch: [CanMatchGuard],data:{allowedRoles:[false,false,true,false,false]}},
      {path:'absences',component:AbsencesSubpage},
      
      
      {path:'timetable',component:TimetableSubpage},

      {path:'presense/:courseID/:starttime/:endtime/:eventID',component:CheckPresenseSubpage},

      {path:'user',component:UserComponent},

      {path:'event',component:EventComponent, canMatch: [CanMatchGuard], data:{allowedRoles:[false,false,true,false,false]}},
    ]
  },
  { path: 'login', component:LoginPage},
  {
    path: '',
    redirectTo: 'home/timetable',
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
