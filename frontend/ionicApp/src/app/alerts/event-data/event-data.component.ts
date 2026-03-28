import {IonHeader,IonToolbar,IonTitle,IonButtons,IonButton,IonContent,IonList,IonItem,IonLabel,IonNote,ModalController} from '@ionic/angular/standalone';
import { Component, Input,OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from "@angular/router";

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

  constructor(private modalController: ModalController,private router: Router) {}

  ngOnInit() {
    // Falls das Datum als String kommt, stellen wir sicher, dass es ein Date-Objekt ist
    // oder wir nutzen die Slice-Methode direkt im HTML.
  }

  dismiss() {
    this.modalController.dismiss();
  }

  presence() {
    console.log(this.event);
    this.modalController.dismiss();
    this.router.navigate(['home/presense',this.event.courseID,this.event.starttime, this.event.endtime, this.event.eventID]);

  }
}


