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
  userID:string;

}
export interface Data{
  exam:Exam;
  grades:Student[];
}

@Component({
  selector: 'app-change-exam',
  templateUrl: './change-exam.subpage.html',
  styleUrls: ['./change-exam.subpage.scss'],
  imports: [FormsModule, IonInput, IonDatetime, IonItem, IonButton, IonDatetimeButton, IonModal, IonList, IonHeader, IonContent, IonToolbar],

})
export class ChangeExamSubpage  implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private api:ApiService) {}
  eventID=0;
  courseID=0;
  data:any={
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
  copyedData:any={
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
  }
  selectedDate: string="";
  formattedDate: string="";
  showDatePicker: boolean = false;

  

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.eventID = params['eventID'];
      this.courseID = params['courseID'];
      this.data.exam.courseID=""+this.courseID;
      this.data.exam.eventID=""+this.eventID;
      console.log(this.eventID);
    });
    this.getData();

  }
  getData(){
    this.api.sendRequestGet({"courseID":this.courseID,"eventID":this.eventID},"getAllGradesFromTest").subscribe( v =>{
      console.log(v);
      this.data=v;
      this.copyedData=this.data;
    })
  }
  sendRequest(){
    }

  
  getTest(){
    if (this.eventID!=0){
      const res = this.api.sendRequestGet({"courseID":this.courseID,"eventID":this.eventID},"getAllGradesFromTest");
      this.data=res;
      this.copyedData=JSON.parse(JSON.stringify(res));
      
    }
  }

  saveChanges(){
    if (this.eventID!=0){
      this.api.sendRequestPost(this.data,"postAllGradesFromAllStudentsOfTest").subscribe({
        next: res =>{
          console.log("saved Succesfully");
          
        },
        error: err => console.error('HTTP Error:', err)
      });
    }else{
      this.api.sendRequestPost(this.data.exam,"addNewTest").subscribe({
        next: res =>{
          console.log("saved Succesfully");
        },
        error: err => console.error('HTTP Error:', err)
      });
    }
    this.getTest();
  }
  deleteTest(){
    console.log(this.copyedData);
    console.log(this.copyedData===this.data);
  }


}
