import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { IonItem, IonList } from "@ionic/angular/standalone";

export interface Absence{
  startdate:string;
  enddate:string;
  starttime:string;
  endtime:string;
  lessons:number;
  eventID:string;
  excused:boolean;
}

@Component({
  selector: 'app-absences',
  templateUrl: './absences.component.html',
  styleUrls: ['./absences.component.scss'],
  imports: [IonItem, IonList],
})
export class AbsencesComponent  implements OnInit {
  absences:Absence[]=[
    {
      startdate:"1234-56-78",
      enddate:"0000-00-00",
      starttime:"12:34",
      endtime:"00:00",
      lessons:10,
      eventID:"0",
      excused:false,
    }
  ]
  constructor(private api:ApiService) {}

  ngOnInit() {}
  parseTime(time:string){
    return time;

  }
  parseDate(date:string){
    return date.slice(8,10)+"."+date.slice(5,7)+"."+date.slice(0,4);

  }
  displayDateTime(absence:Absence){
    if (absence.startdate==absence.enddate){
      return this.parseDate(absence.startdate)+" "+this.parseTime(absence.starttime)+" - "+this.parseTime(absence.endtime);
    }else{
      return this.parseDate(absence.startdate)+" "+this.parseTime(absence.starttime)+" - "+this.parseDate(absence.enddate)+" "+this.parseTime(absence.endtime);

    }

  }
}
