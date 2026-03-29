import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { IonInput, IonModal, IonDatetimeButton, IonItem, IonDatetime, IonButton } from "@ionic/angular/standalone";
import { FormsModule } from '@angular/forms';
import { DropdownComponent } from "src/app/component/dropdown/dropdown.component";
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";

export interface Course{
  courseID: string
  subject: string
  courseName: string
}

export interface EventDetails{
  courseID: string
  courseName:string
  type: number
  description: string
  starttime: string
  endtime: string
  fileID: string
  location: string
}

@Component({
  selector: 'app-event',
  templateUrl: './event.component.html',
  styleUrls: ['./event.component.scss'],
  imports: [IonInput, FormsModule, IonModal, IonDatetimeButton, IonItem, IonDatetime, DropdownComponent, IonButton, FileUploadComponent],
})
export class EventComponent  implements OnInit {

  constructor(private api:ApiService) { }

  eventDetails:EventDetails={
    courseID: "",
    courseName:"Select Course",
    type: 1,
    description: "",
    starttime: "",
    endtime: "",
    fileID: "",
    location: "",
  }

  typeDict:any ={
    "event": 1,
    "sick": 2
  }
  allExists: boolean=false

  courses:Array<Course>=[];

  message:string="safe";

  ngOnInit() {
    this.loadData()

  }
  loadData(){
    this.api.sendRequestGet({},"getCourses").subscribe( v => {
      this.courses=v.courses
      console.log(this.courses)
    })
  }

  checkIfAllExists(){
    this.allExists=(this.eventDetails.courseID.length>5 && this.eventDetails.starttime.length>5);
    console.log(this.eventDetails);
  }
  saveEndtime(event: any){
    this.eventDetails.endtime = event.detail.value.replace("T", " ");
    this.checkIfAllExists();
  }
  saveStarttime(event: any){
    this.eventDetails.starttime = event.detail.value.replace("T", " ");
    this.checkIfAllExists();
  }
  selectCourse(item:any){
    this.eventDetails.courseID=item.courseID;
    this.eventDetails.courseName=item.courseName;
    this.checkIfAllExists();

  }
  saveEvent(){
    this.message="loading";
    this.api.sendRequestPost(this.eventDetails, "addEvent").subscribe(v => {
      this.message="safeed";
    });
  }
  addType(type:string){
    this.eventDetails.type = this.typeDict[type];
  }

}
