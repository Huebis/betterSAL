import { IonHeader, IonToolbar, IonTitle, IonButtons, IonContent, IonButton } from "@ionic/angular/standalone";
import { Component, Input } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { Router } from "@angular/router";

@Component({
  selector: 'app-my-custom-modal',
  templateUrl: './event-data.component.html',
  styleUrls: ['./event-data.component.scss'],
  imports: [IonHeader, IonToolbar, IonTitle, IonButtons, IonButton, IonContent]
})
export class EventDataComponent {
  @Input() event: any;
  @Input() role: any;

  constructor(private modalController: ModalController,
    private router: Router
  ) {}

  presence() {
    console.log(this.event);
    this.modalController.dismiss();
    this.router.navigate(['home/presense',this.event.courseName,this.event.starttime, this.event.endtime, this.event.eventID]);

  }
  close(){
    this.modalController.dismiss();
  }
}

