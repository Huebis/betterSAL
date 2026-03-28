import { CommonModule } from '@angular/common'; // Import CommonModule
import { Component, OnInit } from '@angular/core';
import { IonItem, IonList, IonButton, IonModal, IonDatetimeButton } from "@ionic/angular/standalone";
import { ApiService } from '../../service/api';
import { AlertController } from '@ionic/angular';

import { EventDataComponent } from '../../alerts/event-data/event-data.component'
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/service/auth';
import { FormsModule } from '@angular/forms';

export interface Event{
  starttime:string
  courseID:string
  courseName:string
  endtime:string
  location:string
  subject:string
  type:number
  top:number
  left:number
  width:number
  height:number
};
export interface Day{
  date:string
  schedule:Array<Event>
}
@Component({
  selector: 'app-timetable',
  templateUrl: './timetable.subpage.html',
  styleUrls: ['./timetable.subpage.scss'],
  imports: [CommonModule, FormsModule, IonModal, IonDatetimeButton, IonButton],
  providers: [ModalController]
})
export class TimetableSubpage  implements OnInit {
  days:Array<Day>=[];
  selectedDate:string= new Date().toISOString().slice();
  starttime:string="2026-02-16 08:00";
  endtime:string="2026-02-22 19:00";

  selectedPeriod:string='week';

  elementsShownByType:Array<boolean>=[true,true,true];


  scale:number = 6.60; //11h*60min*0.95
  constructor(private api: ApiService,
    private auth: AuthService,
    private alertController: AlertController,
    private modalController: ModalController) { }
  
  ngOnInit() {
    this.loadData();
  }
  getDate(wantedDate:number){
    if (this.selectedPeriod==="day"){      
      if (wantedDate==1){
        return this.selectedDate.slice(0,10)+" 08:00";
      }else{
        return this.selectedDate.slice(0,10)+" 19:00"
      }
    }else if (this.selectedPeriod==="month"){
      if (wantedDate==1){
        return this.selectedDate.slice(0,8)+"01 08:00"
      }else{
        const currentDate = new Date(this.selectedDate);
        const firstDayNextMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
        const lastDayOfCurrentMonth = new Date(firstDayNextMonth);
        lastDayOfCurrentMonth.setDate(firstDayNextMonth.getDate());
      
        return lastDayOfCurrentMonth.toISOString().slice(0,16).replace('T',' ');
      }
    }else{
      const currentDate = new Date(this.selectedDate);
      const firstDayOfWeek = new Date(currentDate);

      const dayOfWeek = currentDate.getDay();

      firstDayOfWeek.setDate(currentDate.getDate() - currentDate.getDay() + wantedDate);

      return firstDayOfWeek.toISOString().slice(0,16).replace('T',' ');
    }
  }
  loadData(){
    this.days=[]
    this.api.sendRequestGet({},"getSchedule?starttime="+this.getDate(1)+"&endtime="+this.getDate(7)).subscribe(v => {
      console.log(v);
      let weekday = 0;
      if (this.selectedPeriod==='month'){
        const selectedDate = new Date(v.schedule[0].date);
        weekday = (selectedDate.getDay()+6)%7;
        console.log(weekday);
        for (let i=0; i<weekday; i++){
          this.days.push({
            date:"",
            schedule:[]
          })
        }
      }
      for (let i=0; i<v.schedule.length; i++){
        
        this.createDate(v.schedule[i].schedule, i + weekday, v.schedule[i].date);
      };
    });

  }
  createDate(events:Array<any>=[],date:number,dateString:string){
    this.days.push({
      date:dateString,
      schedule:[]
    });
    if (events){
      events.forEach((event) => {
        event.top = this.calculateTimePos(event.starttime);
        event.height = this.calculateTimePos(event.endtime) - event.top;
        event.left = 0;
        event.width = 100;
        console.log(this.days[date])
        this.days[date].schedule.push(event);
        let ammount=0;
        for (let i=this.days[date].schedule.length-2; i>=0; i--){
          ammount++;
          if (this.days[date].schedule[i].top+this.days[date].schedule[i].height <= event.top){
            
            let n=i;
            for (i; i<this.days[date].schedule.length; i++){
              this.days[date].schedule[i].width=100/ammount;
              this.days[date].schedule[i].left=this.days[date].schedule[i].left*(1-1/ammount);
            }
            this.days[date].schedule[this.days[date].schedule.length-1].left = 100-100/ammount;
            this.days[date].schedule[this.days[date].schedule.length-1].width = 100/ammount;
            break;
          }
        }
      })

    }
    
  }

  calculateTime(time:string){
    return (parseInt(time.slice(11,13))*60+parseInt(time.slice(14,16)))/this.scale;
  }
  calculateTimePos(time:string){
    let timePos = this.calculateTime(time)-this.calculateTime(this.starttime);
    if (timePos >= 100){
      return 100;
    }else if (timePos <=0){
      return 0;
    }else{
      return timePos;
    }
  }
  calculateStarttime(time:string):number{
    return 100*(this.calculateTime(time) - this.calculateTime(this.starttime) / this.calculateTime(this.endtime) - this.calculateTime(this.starttime))
  }
  showEventDetail(event:Event){
    this.showAlert(event);
  }
  async showAlert(event:Event) {
    const modal = await this.modalController.create({
        component: EventDataComponent,
        componentProps: {
          event: event,
          role: this.auth.getRole(),
        }
    });
    await modal.present();
  }

  calculateWeekdayLabel(date:string):string{
    let dateObj = new Date(date);
    let options:  Intl.DateTimeFormatOptions = { weekday: 'short' };
    return dateObj.toLocaleDateString('en-US', options);
  }
  calculateDayMonthLabel(date:string):string{
    return date.slice(8,10)+"."+date.slice(5,7)
  }
  selectPeriod(period:string){
    this.selectedPeriod=period;
    console.log(this.getDate(1));
    console.log(this.getDate(7));
    this.loadData();
  }

  changeShown(type:number){

    this.elementsShownByType[type]=!this.elementsShownByType[type];
    if (this.elementsShownByType[type]){
      document.documentElement.style.setProperty('--type'+type+'Display', "absolute");
    }else{
      document.documentElement.style.setProperty('--type'+type+'Display', "none");

    }
  }

}
