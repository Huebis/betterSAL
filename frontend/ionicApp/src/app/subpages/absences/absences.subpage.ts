import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { DropdownComponent } from "../../component/dropdown/dropdown.component";
import { IonCheckbox } from "@ionic/angular/standalone";
import { FormsModule } from '@angular/forms';
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";
import { FileDownloadComponent } from "src/app/component/file-download/file-download.component";
import { IonicModule } from "@ionic/angular";
import { Head } from 'rxjs';


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
  selected: boolean
}
export interface User{
  firstName:string
  lastName: string
  excused:Array<Absence>
  finished:Array<Absence>
  notExcused:Array<Absence>
}

export interface HeaderItems{
  change:boolean
  merge:boolean
  somethingChanged:boolean
}

@Component({
  selector: 'app-absences',
  templateUrl: './absences.subpage.html',
  styleUrls: ['./absences.subpage.scss'],
  imports: [DropdownComponent, FormsModule, FileUploadComponent, FileDownloadComponent, IonicModule],
})
export class AbsencesSubpage  implements OnInit {
  data:any;
  header:any;
  itemSelectors:any;

  mergeList:Array<String>=[]

  test=false;

  absences:User= {
    firstName: "",
    lastName: "",
    excused: [],
    finished: [],
    notExcused: []
  };
  headerItems:HeaderItems = {
    change: false,
    merge: false,
    somethingChanged : true
  }

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

  activateMerge(item:any){
    if (item.merge){
      let data:any={
        absenceIDList:[]
      }
      this.api.sendRequestPost(data,"absence?requestType=merge").subscribe();
      item.merge=false;
    }else{
      item.merge=true;
      item.change=false;
    }
  }
  activateChange(item:any){
    if (item.change){
      item.change=false;
    }else{
      item.change=true;
      item.merge=false;
    }
  }
  safe(item:any){
    this.api.sendRequestPost(item,"absence?requestType=change").subscribe();
    item.change=false;
  }
  changeExcused(event: CustomEvent, item:any){
    item.excused = event.detail.value;
    
  }



}
