import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { IonButton, IonItem, IonLabel,  IonList, IonItemGroup} from '@ionic/angular/standalone';

import { ApiService } from '../../service/api';
import { DropdownComponent } from "src/app/component/dropdown/dropdown.component";

export interface Grade{
  date:string;
  fileID:string;
  grade:number;
  message:string;
  testName:string;
  weight:number;
};
export interface Subject{
  grades: Grade[];
  name:string;
};

@Component({
  selector: 'app-grades',
  templateUrl: './grades.subpage.html',
  styleUrls: ['./grades.subpage.scss'],
  imports: [IonButton, IonItem, IonList, CommonModule, IonLabel, DropdownComponent],
})
export class GradesSubpage  implements OnInit {

  constructor(private api: ApiService) { }

  subjects:Array<Subject> = [];

    
    ngOnInit() {
      this.loadData();
    }

    loadData(){
      this.api.sendRequestGet({},"getGradesStudent").subscribe(v => {
        this.subjects=v.subjects;
        console.log(v);
      });

    };
    getAverage(grades:Grade[]){
      console.log(grades);
      let average=0;
      let amount=0;
      console.log(Array.isArray(grades))
      grades.forEach(exam => {if (exam.grade!=0){average+=exam.grade*exam.weight; amount+=exam.weight}});
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

