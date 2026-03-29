import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { TimeDisplayComponent } from "src/app/component/time-display/time-display.component";
import { FileDownloadComponent } from "src/app/component/file-download/file-download.component";
import { DropdownComponent } from "src/app/component/dropdown/dropdown.component";
import { IonButton } from "@ionic/angular/standalone";

export interface Student{
  firstName:string
  lastName:string
  userID:string
  excused:Array<any>
  notExcused:Array<any>
  finished:Array<any>
}

@Component({
  selector: 'app-teacher-absences',
  templateUrl: './teacher-absences.subpage.html',
  styleUrls: ['./teacher-absences.subpage.scss'],
  imports: [TimeDisplayComponent, FileDownloadComponent, DropdownComponent, IonButton],
})
export class TeacherAbsencesSubpage  implements OnInit {

  absences:Array<Student>=[]

  constructor(private api:ApiService) { }

  ngOnInit() {
    this.loadData();
  }

  loadData(){
    this.api.sendRequestGet({},"absence").subscribe(v => {
      console.log(v);
      this.absences=v.absence;
      console.log(this.absences)
    });
  }
  sendData(item:any){
    this.api.sendRequestPost(item,"absence?requestType=change").subscribe();
    item.change=false;
    this.loadData();
  }

}
