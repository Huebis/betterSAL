import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, 
  IonCard, IonCardHeader, IonCardTitle, IonCardContent, 
  IonItem, IonLabel, IonInput, IonButton, IonIcon, IonText,IonAccordion, IonAccordionGroup 
} from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { checkmarkCircleOutline, eyeOutline, eyeOffOutline, bookOutline } from 'ionicons/icons';
import { VideoComponent } from '../video/video.component';

interface Aufgabe {
  frage: string;
  antwort: string;
  userEingabe?: string;
  geloest?: boolean;
  zeigeLoesung?: boolean;
  istFalsch?: boolean;
}

interface Lerneinheit {
  titel: string;
  beschreibung: string; // Dein Text zur Exercise
  aufgaben: Aufgabe[];
}

@Component({
  selector: 'app-eliah-exercise-test',
  templateUrl: './eliah-exercise-test.component.html',
  styleUrls: ['./eliah-exercise-test.component.scss'],
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    IonHeader, IonToolbar, IonTitle, IonContent, 
    IonCard, IonCardHeader, IonCardTitle, IonCardContent, 
    IonItem, IonLabel, IonInput, IonButton, IonIcon, IonText,IonAccordion, IonAccordionGroup, VideoComponent
  ]
})
export class EliahExerciseTestComponent  implements OnInit {


  ngOnInit() {}

uebungen: Lerneinheit[] = [
    {
      titel: 'Exercise 1',
      beschreibung: 'Rechne zusammen',
      aufgaben: [
        { frage: 'Was ist 15 + 25?', antwort: '40' },
        { frage: 'Was ist 100 - 45?', antwort: '55' }
      ]
    },
    {
      titel: 'Exercise 2',
      beschreibung: 'Europa besteht aus vielen Ländern. Die größten Städte sind oft die Hauptstädte.',
      aufgaben: [
        { frage: 'Hauptstadt von Deutschland?', antwort: 'Berlin' },
        { frage: 'In welchem Land liegt Rom?', antwort: 'Italien' }
      ]
    }
  ];

  constructor() {
    addIcons({ checkmarkCircleOutline, eyeOutline, eyeOffOutline, bookOutline });
  }

  checkLoesung(aufgabe: Aufgabe) {
    const korrekteAntwort = aufgabe.antwort.toLowerCase().trim();
    const userAntwort = aufgabe.userEingabe?.toLowerCase().trim();

    if (userAntwort === korrekteAntwort) {
      aufgabe.geloest = true;
      aufgabe.istFalsch = false;
    } else {
      aufgabe.geloest = false;
      aufgabe.istFalsch = true;

      // Nach 3 Sekunden (3000ms) den Status wieder zurücksetzen
      setTimeout(() => {
        aufgabe.istFalsch = false;
      }, 3000);
    }
  }

  toggleLoesung(aufgabe: Aufgabe) {
    aufgabe.zeigeLoesung = !aufgabe.zeigeLoesung;
  }
}