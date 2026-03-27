import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-time-display',
  templateUrl: './time-display.component.html',
  styleUrls: ['./time-display.component.scss'],
})
export class TimeDisplayComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}

  @Input() starttime: any = "";
  @Input() endtime:any = "";

  
}
