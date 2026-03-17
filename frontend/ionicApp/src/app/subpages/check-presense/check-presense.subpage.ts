import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/service/api';
import { IonicModule } from "@ionic/angular";
import { FormsModule } from '@angular/forms';


export interface User{
  absence: number
  firstName: string
  lastName: string
  userID: string
  isPresent: boolean
}

@Component({
  selector: 'app-check-presense',
  templateUrl: './check-presense.subpage.html',
  styleUrls: ['./check-presense.subpage.scss'],
  imports: [IonicModule, FormsModule],
})
export class CheckPresenseSubpage  implements OnInit {
  students:Array<User>=[
    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    },    {firstName:"test",
      lastName:"test",
      absence:0,
      userID:"oeoe",
      isPresent:false
    }
  ];
  courseID:string="";
  starttime:string="";
  endtime:string="";
  eventID:string="";
  somethingChanged:boolean = false;
  sumOfPresentStudents:number = 0;


  constructor(private api:ApiService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(params =>{
      this.courseID = params['courseID'];
      this.starttime = params['starttime'];
      this.endtime = params['endtime'];
      this.eventID = params['eventID'];
      this.loadData();
    });
  }

  loadData(){
    this.api.sendRequestGet({
      courseID: this.courseID,
      starttime: this.starttime,
      endtime: this.endtime,
      eventID: this.eventID
    }, "presenceList").subscribe(v => {
      this.students = v.anwesenheitsliste.map((v:any) => {
        v.isPresent = (v.absence==0); return v
      })
      this.checkChanged();
    })
  }
  safePresenseList(){
    console.log({lesson:{
      courseID: this.courseID,
      starttime: this.starttime,
      endtime: this.endtime,
      eventID: this.eventID},
    anwesenheitsliste:this.students.map(student => {
    if (student.isPresent){
      return student;
    }else{
      if (student.absence===0){
        student.absence=1//not excusable
      }
      return student;
    }})});
    this.api.sendRequestPost({
      lesson:{
        courseID: this.courseID,
        starttime: this.starttime,
        endtime: this.endtime,
        eventID: this.eventID},
      anwesenheitsliste:this.students.map(student => {
      if (student.isPresent){
        return student;
      }else{
        if (student.absence===0){
          student.absence=1//not excusable
        }
        return student;
      }
    })},"presenceList").subscribe(v => {
      console.log(v);
      this.students=v;
      this.somethingChanged = true;
    });
    this.somethingChanged = true;
  }
  checkChanged(){
    this.somethingChanged = false;
    this.sumOfPresentStudents = 0;
    this.students.forEach(v => {v.isPresent ? this.sumOfPresentStudents+=1 : 0} )
    console.log(this.sumOfPresentStudents)
  }


}
