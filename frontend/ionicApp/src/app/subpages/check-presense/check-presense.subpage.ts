import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/service/api';

@Component({
  selector: 'app-check-presense',
  templateUrl: './check-presense.subpage.html',
  styleUrls: ['./check-presense.subpage.scss'],
})
export class CheckPresenseSubpage  implements OnInit {
  students:Array<any>=[];
  courseID:string="";
  starttime:string="";
  endtime:string="";
  eventID:string="";


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
      console.log(v);
      this.students = v;
    })
  }
  safePresenseList(){
    this.api.sendRequestPost(this.students,"presenceList").subscribe(v => {
      console.log(v);
      this.students=v;
    });
  }


}
