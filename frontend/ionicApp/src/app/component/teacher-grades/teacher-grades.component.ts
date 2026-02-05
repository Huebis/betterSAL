import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { IonButton, IonItem, IonLabel,  IonList, IonItemGroup} from '@ionic/angular/standalone';

import { ApiService } from '../../service/api';
import { Router } from '@angular/router';

export interface Exam{
  date:string;
  testName:string;
  weight:number;
  eventID:string;
};
export interface Course{
  grades: Exam[];
  name:string;
};
@Component({
  selector: 'app-teacher-grades',
  templateUrl: './teacher-grades.component.html',
  styleUrls: ['./teacher-grades.component.scss'],
  imports: [IonButton, IonItem, IonList, CommonModule,IonLabel],

})
export class TeacherGradesComponent  implements OnInit {

  constructor(private api: ApiService, private router: Router) { }

  classes: any[] = [];
  
  
  getClass() {
    this.api.sendRequestGet({},"/getAllTests").subscribe({
      next: res => {
        
        this.classes=res.courses.map((v:any) => {
          v.exams.map( (v: any) =>{
            v.open=false; return v;
          });
          return v;
        })
        console.log(this.classes);
          
      },
      error: err => console.error('HTTP Error:', err)
    });
  }
  ngOnInit() {
    this.getClass();
  }

  toggleClass(subject:any){
    subject.open=!subject.open;
    console.log(this.classes);
  }
  editGrade(courseID:string,eventID:string){  
    this.router.navigate(['home/changeExam',courseID,eventID]);
  };



}
