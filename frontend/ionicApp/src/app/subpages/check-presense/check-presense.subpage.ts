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

  constructor(private api:ApiService, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(params =>{
      this.api.sendRequestGet({
        courseName: params['courseName'],
        starttime: params['starttime'],
        endtime: params['endtime'],
        eventID: params['eventID']
      },"presenceList").subscribe(v => {
        console.log(v);
        this.students=v;
      });
    });
    
  }
  safePresenseList(){
    this.api.sendRequestPost(this.students,"presenceList").subscribe(v => {
      console.log(v);
      this.students=v;
    });
  }


}
