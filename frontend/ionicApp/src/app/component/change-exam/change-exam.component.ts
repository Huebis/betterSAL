import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';


import { IonInput, IonDatetime, IonItem, IonLabel, IonButton, IonIcon, IonDatetimeButton, IonModal, IonList } from '@ionic/angular/standalone';
import { ApiService } from 'src/app/service/api';



export interface Exam{
  date:string;
  description:string;
  endtime:string;
  starttime:string;
  location:string;
  testName:string;
  weight:number;
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
  imports: [FormsModule, IonInput, IonDatetime, IonItem, IonLabel, IonButton, IonIcon, IonDatetimeButton, IonModal, IonList],

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
      weight:1
    },
    grades:[
      {
        fileID:"1",
        firstName:"Eliah",
        lastName:"Huebis",
        grade:1,
        message:"test"
      }
    ]

  };
  selectedDate: string="";
  formattedDate: string="";
  showDatePicker: boolean = false;

  

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.eventID = params['eventID'];
      this.courseID = params['courseID'];
    });
    this.api.sendRequestGet({"courseID":this.courseID,"eventID":this.eventID},"/getAllGradesFromTest").subscribe({
      next: res => {
        this.data=res;
        console.log(this.data);
      },
      error: err => console.error('HTTP Error:', err)
    });
  }

  highlightedDates = [(isoString: string) => {
    const date = new Date(isoString);
    const utcDay = date.getUTCDate()-2;

    if (utcDay % 7 === 0) {//lessons
      return {
        backgroundColor: '#00ff3717',
        border: '1px solid #00ff0075',
      };
    }
    if (utcDay % 7 === 2) {//tests
      return {
        backgroundColor: '#ff000017',
        border: '1px solid #ff000075',
      };
    }
    return undefined;
  },
  {
    date: '2026-02-05',
    textColor: '#800080',
    backgroundColor: '#ffc0cb',
    border: '1px solid #e91e63',
  },
]
 printData(){
  console.log(this.data);
 }
 
 openDatePicker() {
  this.showDatePicker = true;
}

formatDate() {
  if (this.selectedDate) {
    const date = new Date(this.selectedDate);
    this.formattedDate = `${('0' + date.getDate()).slice(-2)}, ${('0' + (date.getMonth() + 1)).slice(-2)}, ${date.getFullYear()}`;
    this.showDatePicker = false; // Close the date picker after selection
  }
}
}
