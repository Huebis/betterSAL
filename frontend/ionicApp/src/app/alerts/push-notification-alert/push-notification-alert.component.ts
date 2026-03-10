import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-push-notification-alert',
  templateUrl: './push-notification-alert.component.html',
  styleUrls: ['./push-notification-alert.component.scss'],
})
export class PushNotificationAlertComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}
  @Input() input: any;

  print(){
    console.log(this.input);
  }

}
