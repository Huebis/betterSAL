import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { IonButton, IonItem, IonLabel,  IonList, IonItemGroup} from '@ionic/angular/standalone';

import { ApiService } from '../../service/api';

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
  imports: [IonButton, IonItem, IonList, CommonModule,IonLabel],
})
export class GradesComponent  implements OnInit {

  constructor(private api: ApiService) { }

  subjects: any[] = [
    {name:"test",open:false,grades:[
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""},
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""}
    ]},
    {name:"test",open:false,grades:[
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""},
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""}
    ]},
    {name:"test",open:false,grades:[
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""},
      {date:"1",testName:"2",message:"3",weight:4,grade:5,fileId:""}
    ]}
  ];

    
    getSubjects() {
      this.api.sendRequestGet({},"/getGradesStudent").subscribe({
        next: res => {
          this.subjects=res.subjects.map((v:any) => {
            v.grades.map( (v: any) =>{
              v.open=false; return v;
            });
            return v;
          })
          console.log(this.subjects);
            
        },
        error: err => console.error('HTTP Error:', err)
      });
    }
    ngOnInit() {
      this.getSubjects();
    }
    getAverage(grades:grade[]){
      let average=0;
      let amount=0;
      console.log(Array.isArray(grades))
      grades.forEach(exam => {average+=exam.grade*exam.weight; amount+=exam.weight});
      return Math.floor(average/amount*100)/100;
    }
    getFile(fileId:string){
      console.log(fileId);
    }
    toggleSubject(subject:any){
      subject.open=!subject.open;
      console.log(this.subjects);
    }
  
  }

