import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { IonToggle, IonButton } from "@ionic/angular/standalone";
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';

export interface User{
  className:string
  email:string
  firstName:string
  lastName:string
  major:string
  notifAbsenceDueTomorrow:boolean
  notifAbsenceOfTeacherToday:boolean 
  notifAbsenceOfTeacherTomorrow:boolean
  notifEventTomorrow:boolean
  notifExamTomorrow:boolean
  notifGradeChange:boolean
  role:number
  userName:string
}

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.scss'],
  imports: [FormsModule, IonButton],
})
export class UserComponent  implements OnInit {
  user:User={
    className:"",
    email:"",
    firstName:"",
    lastName:"",
    major:"",
    notifAbsenceDueTomorrow:false,
    notifAbsenceOfTeacherToday:false, 
    notifAbsenceOfTeacherTomorrow:false,
    notifEventTomorrow:false,
    notifExamTomorrow:false,
    notifGradeChange:false,
    role:0,
    userName:"",
  };

  somethingChanged = true;
  editUserInformations=false;
  test:string="blabla";

  constructor(private api: ApiService) { }

  ngOnInit() {
    this.loadData();
  }

  loadData(){
    this.api.sendRequestGet({},"getUserData").subscribe(v => {
      console.log(v);
      this.user=v;
    });

  }
  safe(){
    console.log(this.somethingChanged);
    this.api.sendRequestPost(this.user,"postUserData").subscribe();
    this.somethingChanged = true;
  }
  editUserInformation(){
    this.editUserInformations = (this.editUserInformations==false);
    console.log(this.editUserInformations);
  }

}
