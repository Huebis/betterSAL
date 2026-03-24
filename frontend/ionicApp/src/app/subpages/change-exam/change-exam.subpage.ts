import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';


import { IonInput, IonDatetime, IonItem, IonButton, IonDatetimeButton, IonModal, IonList, IonHeader, IonContent, IonToolbar } from '@ionic/angular/standalone';
import { ApiService } from 'src/app/service/api';
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";



export interface Exam{
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
  imports: [FormsModule, IonInput, IonDatetime, IonItem, IonButton, IonDatetimeButton, IonModal, IonList, IonHeader, IonContent, IonToolbar, FileUploadComponent],

})
export class ChangeExamSubpage  implements OnInit {

  constructor(private route: ActivatedRoute, private router: Router, private api:ApiService) {}
  eventID=0;
  courseID=0;
  data:any={
    exam:{
      description:"description",
      endtime:"2000-01-01T00:00",
      starttime:"2000-01-01T00:00",
      location:"000",
      testName:"Test",
      weight:1,
      courseID:"",
      eventID:"",
    },
    grades:[]
  };
  somethingChanged=false;
  starttime="2000-01-01T00:00:00";
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
    if (this.eventID!==0){
      this.getData();
    }

  }
  getData(){
    this.api.sendRequestGet({"courseID":this.courseID,"eventID":this.eventID},"getAllGradesFromTest").subscribe( v =>{
      v.exam.starttime = v.exam.starttime.replace(" ","T");
      v.exam.endtime = v.exam.endtime.replace(" ","T");
      console.log(v.exam.endtime.replace(" ","T"));
      this.data=v;
      console.log(this.data)
      
      this.somethingChanged=true;
    })
  }
  sendRequest(){
    }

  saveChanges(){
    this.data.exam.starttime = this.data.exam.starttime.replace("T"," ").slice(0,16);
    this.data.exam.endtime = this.data.exam.starttime.slice(0,10)+" "+this.data.exam.endtime.slice(11,16);
    if (this.eventID!=0){
      console.log(this.data);
      
      this.api.sendRequestPost(this.data,"postAllGradesFromAllStudentsOfTest").subscribe({
        next: res =>{
          console.log("saved Succesfully");
          this.getData();
          
          
        },
        error: err => console.error('HTTP Error:', err)
      });
    }else{
      console.log("blabla");
      this.api.sendRequestPost(this.data.exam,"addNewTest").subscribe({
        next: res =>{
          console.log("saved Succesfully");
          this.router.navigate(["/home/grades"]);
        },
        error: err => console.error('HTTP Error:', err)
      });
    }
   
  }
  deleteTest(){
    this.api.sendRequestPost(this.data.exam,"deleteTest").subscribe( v => {
      this.router.navigate(["/home/grades"]);
    });
    console.log(this.data);
  }


}
