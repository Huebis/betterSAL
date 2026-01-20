import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';


import { ApiService } from '../api.service';

interface gradeInformation{
  grade: number;
  date: string;
  message: string;
  fileId: string;
}


@Component({
  selector: 'app-grades',
  imports: [CommonModule],
  templateUrl: './grades.html',
  styleUrl: './grades.css',
})


export class GradesComponent {
  constructor( private api: ApiService){};
  //subjects$: Observable<any> = this.api.sendRequest({},"get_grades_student");
  subjects=[
    {name:"M",
      grades:[
        {
          grade:6,
          date:"01.01.2025",
          message:"nothing",
          fileId:"xy"
        },{
          grade:6,
          date:"01.01.2025",
          message:"nothing",
          fileId:"xy"
        }
      ]
    }
  ]

  getAverage(grades:Array<gradeInformation>){
    let sum=0;
    for (let i=0; i<grades.length; i++){
      sum += grades[i].grade;
    };
    return Math.round(sum/grades.length)

  }
}
