import {IonHeader,IonToolbar,IonTitle,IonButtons,IonButton,IonContent,IonList,IonItem,IonLabel,IonNote,ModalController} from '@ionic/angular/standalone';
import { Component, Input,OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from "@angular/router";
import { ApiService } from 'src/app/service/api';

@Component({
  selector: 'app-event-data',
  templateUrl: './event-data.component.html',
  styleUrls: ['./event-data.component.scss'],
  standalone: true,
  imports: [CommonModule,IonHeader,IonToolbar,IonTitle,IonButtons,IonButton,IonContent,IonList,IonItem,IonLabel,IonNote]
})
export class EventDataComponent implements OnInit {
  // Das 'event' Objekt wird von der Hauptseite übergeben
  @Input() event: any;
  @Input() role: any;

  constructor(private modalController: ModalController,private router: Router,private api:ApiService) {}

  ngOnInit() {

  }

  dismiss() {
    this.modalController.dismiss();
  }

  presence() {
    console.log(this.event);
    this.modalController.dismiss();
    this.router.navigate(['home/presense',this.event.courseID,this.event.starttime, this.event.endtime, this.event.eventID]);

  }
  changeEventToSickTeacher(){
    let data:any={
        courseID: this.event.courseID,
        eventID: this.event.eventID,
        type: 450,
        description: this.event.description ?? '',
        starttime: this.event.starttime,
        endtime: this.event.endtime,
        location: this.event.location,
        fileID: this.event.fileID ?? ''
      }
      console.log(data)
      this.api.sendRequestPost(data,"addEvent").subscribe();
      this.modalController.dismiss({ refreshed: true });
  }

    cancelLection(){
    let data:any={
        courseID: this.event.courseID,
        eventID: this.event.eventID,
        type: 400,
        description: this.event.description ?? '',
        starttime: this.event.starttime,
        endtime: this.event.endtime,
        location: this.event.location,
        fileID: this.event.fileID ?? ''
      }
      console.log(data)
      this.api.sendRequestPost(data,"addEvent").subscribe();
      this.modalController.dismiss({ refreshed: true });
  }
}


