import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { DropdownComponent } from "../../component/dropdown/dropdown.component";

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
  templateUrl: './absences.subpage.html',
  styleUrls: ['./absences.subpage.scss'],
  imports: [DropdownComponent],
})
export class AbsencesSubpage  implements OnInit {
  data:any;
  header:any;
  itemSelectors:any;

  absences:Absence[]=[
    {
      startdate:"1234-56-78",
      enddate:"0000-00-00",
      starttime:"12:34",
      endtime:"00:00",
      lessons:10,
      eventID:"0",
      excused:false,
    },{
      startdate:"1234-56-78",
      enddate:"0000-00-00",
      starttime:"12:34",
      endtime:"00:00",
      lessons:10,
      eventID:"0",
      excused:false,
    },
  ]
  constructor(private api:ApiService) {}

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

  ngOnInit() {
    this.data=this.absences
    this.header=[{
      text:"Absencen",
      type:"text",
    }]
    this.itemSelectors=[
      {
        selector:"startdate",
        type:"input",
        function:false,
        param:(item:any)=>{return item.excused},
      },
      {
        selector:"enddate",
        type:"text",
        function:(param:any)=>console.log(this.data),
        param:(item:any)=>{return item.excused},
      }
    ]
    this.api.sendRequestGet({},"absence").subscribe(v => {
      console.log(v);
    });





  }



}
