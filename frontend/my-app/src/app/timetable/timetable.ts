import { Component } from '@angular/core';

@Component({
  selector: 'app-timetable',
  imports: [],
  templateUrl: './timetable.html',
  styleUrl: './timetable.css',
})
export class TimetableComponent {
  lessons=[{
    subject:"M",
    teacher:"Warin",
    room:"200",
    day:0,
    startTime:900,
    endTime:1800}];
  startTime=800;
  scale=2000.0/2400.0;
  width=100;
  
  translateDay(day:number){
    console.log(day*this.width);
    return day*this.width;
  }
  calculateStartTime(time:number){
    console.log(Math.floor((time-this.startTime)*this.scale));
    return Math.floor((time-this.startTime)*this.scale);
  }
  calculateHeight(startTime:number,endTime:number){
    console.log(Math.floor((endTime-startTime)*this.scale));
    return Math.floor((endTime-startTime)*this.scale);
  }
}
