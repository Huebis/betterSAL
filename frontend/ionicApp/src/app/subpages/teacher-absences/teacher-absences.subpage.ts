import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { DropdownComponent } from "../../component/dropdown/dropdown.component";
import { FormsModule } from '@angular/forms';
import { FileUploadComponent } from "src/app/component/file-upload/file-upload.component";
import { FileDownloadComponent } from "src/app/component/file-download/file-download.component";
import { TimeDisplayComponent } from "src/app/component/time-display/time-display.component";
import { DatePipe, CommonModule } from '@angular/common';


import { 
  IonCheckbox, 
  IonButton, 
  IonInput, 
  IonCol, 
  IonRow, 
  IonGrid, 
  IonBadge, 
  IonIcon 
} from "@ionic/angular/standalone";

export interface Event {
  courseName: string;
  endtime: string;
  starttime: string;
  subject: string;
  eventID: string;
  location: string;
}

export interface Absence {
  absenceID: string;
  discription: string;
  endday: string;
  events: Array<Event>;
  excused: number;
  fileID: string;
  length: number;
  selected: boolean;
  change?: boolean; 
}

export interface User {
  firstName: string;
  lastName: string;
  excused: Array<Absence>;
  finished: Array<Absence>;
  notExcused: Array<Absence>;
}

export interface HeaderItems {
  change: boolean;
  merge: boolean;
  somethingChanged: boolean;
}

@Component({
  selector: 'app-teacher-absences',
  templateUrl: './teacher-absences.subpage.html',
  styleUrls: ['./teacher-absences.subpage.scss'],
  standalone: true,
  imports: [
    DropdownComponent, 
    FormsModule, 
    FileUploadComponent, 
    FileDownloadComponent, 
    TimeDisplayComponent, 
    IonButton, 
    IonCheckbox, 
    IonInput, 
    IonCol, 
    IonRow, 
    IonGrid, 
    IonBadge, 
    IonIcon,
    DatePipe, 
    CommonModule
  ],
})
export class TeacherAbsencesSubpage implements OnInit {
  
  students: Array<User> = []; 

  headerItems: HeaderItems = {
    change: false,
    merge: false,
    somethingChanged: true
  };

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.api.sendRequestGet({}, "absence").subscribe(v => {
      console.log("API Response:", v);
      this.students = v.absence || []; 
    });
  }

  activateMerge(headerItems: any, student: User) {
    if (headerItems.merge) {
      let data: any = {
        absenceIDList: []
      };

      student.notExcused.forEach((v: any) => {
        if (v.selected) {
          data.absenceIDList.push(v.absenceID);
        }
      });

      this.api.sendRequestPost(data, "absence?requestType=merge").subscribe(() => {
        headerItems.merge = false;
        this.loadData();
      });
    } else {
      headerItems.merge = true;
      headerItems.change = false;
    }
  }

  safe(item: any) {
    this.api.sendRequestPost(item, "absence?requestType=change").subscribe(() => {
      item.change = false;
      this.loadData();
    });
  }

  parseDate(date: string) {
    return date.slice(8, 10) + "." + date.slice(5, 7) + "." + date.slice(0, 4);
  }
}