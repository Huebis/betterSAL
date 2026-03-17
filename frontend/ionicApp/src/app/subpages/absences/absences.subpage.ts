import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { DropdownComponent } from "../../component/dropdown/dropdown.component";

export interface Event{
  courseName: string
  endtime: string
  starttime: string
  subject: string
  eventID: string
  location:string
}
export interface Absence{
  absenceID:string
  discription: string
  endday: string
  events: Array<Event>
  excused: number
  fileID: string
  length: number
}
export interface User{
  firstName:string
  lastName: string
  excused:Array<Absence>
  finished:Array<Absence>
  notExcused:Array<Absence>
}

@Component({
  selector: 'app-absences',
  templateUrl: './absences.subpage.html',
  styleUrls: ['./absences.subpage.scss'],
  imports: [DropdownComponent],
})
export class AbsencesSubpage  implements OnInit {
  data:any;
  header:any;
  itemSelectors:any;

  absences:User= {
    firstName: "",
    lastName: "",
    excused: [],
    finished: [],
    notExcused: []
  };

  constructor(private api:ApiService) {}

  parseTime(time:string){
    return time;

  }
  parseDate(date:string){
    return date.slice(8,10)+"."+date.slice(5,7)+"."+date.slice(0,4);

  }

  ngOnInit() {

    this.api.sendRequestGet({},"absence").subscribe(v => {
      console.log(v);
      this.absences=v.absence[0];
    });





  }



}
