import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';


import { IonInput, IonDatetime, IonItem, IonButton, IonDatetimeButton, IonModal, IonList, IonHeader, IonContent, IonToolbar } from '@ionic/angular/standalone';
import { ApiService } from 'src/app/service/api';



export interface Exam{
  date:string;
  description:string;
  endtime:string;
  starttime:string;
  location:string;
  testName:string;
  weight:number;
  courseID:string;
  eventID:string;

}
export interface Student{
  fileID:string;
  firstName:string;
  lastName:string;
  grade:number;
  message:string;

}
export interface Data{
  exam:Exam;
  grades:Student[];
}

@Component({
  selector: 'app-change-exam',
  templateUrl: './change-exam.component.html',
  styleUrls: ['./change-exam.component.scss'],
  imports: [FormsModule, IonInput, IonDatetime, IonItem, IonButton, IonDatetimeButton, IonModal, IonList, IonHeader, IonContent, IonToolbar],

})
export class ChangeExamComponent  implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private api:ApiService) {}
  eventID=0;
  courseID=0;
  data:Data={
    exam:{
      date:"2000-01-01",
      description:"description",
      endtime:"00:00",
      starttime:"00:00",
      location:"000",
      testName:"Test",
      weight:1,
      courseID:"",
      eventID:"",
    },
    grades:[]

  };
  selectedDate: string="";
  formattedDate: string="";
  showDatePicker: boolean = false;

  

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.eventID = params['eventID'];
      this.courseID = params['courseID'];
      this.data.exam.courseID=""+this.courseID;
      this.data.exam.eventID=""+this.courseID;
      console.log(this.eventID)
    });
    this.api.sendRequestGet({"courseID":this.courseID,"eventID":this.eventID},"/getAllGradesFromTest").subscribe({
      next: res => {
        this.data=res;
        console.log(this.data);
      },
      error: err => console.error('HTTP Error:', err)
    });
  }

  saveChanges(){
    if (this.eventID!=0){
      this.api.sendRequestPost(this.data,"/saveExam").subscribe({
        next: res =>{
          console.log("saved Succesfully");
        },
        error: err => console.error('HTTP Error:', err)
      });
    }else{
      this.api.sendRequestPost(this.data.exam,"/createExam").subscribe({
        next: res =>{
          console.log("saved Succesfully");
        },
        error: err => console.error('HTTP Error:', err)
      });
    }
  }

}
