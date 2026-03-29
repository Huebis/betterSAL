import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonButton} from '@ionic/angular/standalone';
import { ApiService } from '../../service/api';
import { Router } from '@angular/router';
import { DropdownComponent } from "src/app/component/dropdown/dropdown.component";

export interface Exam{
  date:string;
  testName:string;
  weight:number;
  eventID:string;
};
export interface Course{
  grades: Exam[];
  name: string;
};
@Component({
  selector: 'app-teacher-grades',
  templateUrl: './teacher-grades.subpage.html',
  styleUrls: ['./teacher-grades.subpage.scss'],
  imports: [CommonModule, DropdownComponent,IonButton],

})
export class TeacherGradesSubpage  implements OnInit {

  constructor(private api: ApiService, private router: Router) { }

  courses: any[] = [];
  
  
  
  getClass() {
    this.api.sendRequestGet({},"/getAllTests").subscribe(v => {
      v.courses.map((v:any) => {
        v.exams.map( (v: any) =>{
          v.open=false; return v;
        });
        return v;
      })
    });
  }

  ngOnInit() {
    this.getData();
  }
  getData(){
    this.api.sendRequestGet({},"getAllTests").subscribe(v => {
      console.log(v);
      this.courses=v.courses;
    });
  }

  toggleClass(subject:any){
    subject.open=!subject.open;
    console.log(this.courses);
  }
  editGrade(courseID:string,eventID:string){  
    this.router.navigate(['home/changeExam',courseID,eventID]);
  };


}
