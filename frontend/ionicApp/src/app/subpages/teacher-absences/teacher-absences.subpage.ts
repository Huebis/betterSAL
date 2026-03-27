import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';

export interface Student{
  firstName:string
  lastName:string
  userID:string
  excused:Array<any>
}

@Component({
  selector: 'app-teacher-absences',
  templateUrl: './teacher-absences.subpage.html',
  styleUrls: ['./teacher-absences.subpage.scss'],
})
export class TeacherAbsencesSubpage  implements OnInit {

  absences:Array<Student>=[]

  constructor(private api:ApiService) { }

  ngOnInit() {
    this.loadData();
  }

  loadData(){
    this.api.sendRequestGet({},"absence").subscribe(v => {
      console.log(v);
      this.absences=v.absence[0];
    });
  }

}
