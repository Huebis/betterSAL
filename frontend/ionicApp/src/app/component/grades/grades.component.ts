import { Component, OnInit } from '@angular/core';

import { ApiService } from '../../service/api';

import { Observable } from 'rxjs';



export interface grade{
  date:string;
  fileID:string;
  grade:number;
  message:string;
  testName:string;
  weight:number;
};
export interface subject{
  grades: grade[];
  name:string;
};


@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrls: ['./grades.component.scss'],
})
export class GradesComponent  implements OnInit {
  
  

  constructor(private api: ApiService) { }

  subjects: any[] = [];
  getSubjects() {
    this.api.sendRequest({},"/getGradesStudent").subscribe(v => {this.subjects=v.grades; console.log(v.grades)});
  }
  ngOnInit() {
    this.getSubjects();
  }
  getAverage(grades:grade[]){
    let average=0;
    let amount=0;
    grades.forEach(grade => {average+=grade.grade*grade.weight; amount+=grade.weight});
    return Math.round(average/amount*100)/100;
  }
  getFile(fileId:string){
    console.log(fileId);
  }

}
