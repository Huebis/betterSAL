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
      beschreibung: 'Rewrite the sentences to make conditional sentences.',
      aufgaben: [
        { frage: 'I make films that appeal to both children and adults, as they do better at the box office. If I make ...', antwort: 'If I make films that appeal to both children and adults, they do better at the box office.' },
        { frage: "The director has a dark imagination and is considering an unhappy ending. If the director didn't ...", antwort: "If the director didn't have a dark imagination, he wouldn’t be considering an unhappy ending." },
        { frage: "I didn't see the film, so I couldn't join in the discussion. I could ...", antwort: 'I could have joined in the discussion if I had seen the film.' },
        { frage: "A film can contain violent images, but audiences are usually warned by the cinema. Audiences will ...", antwort: 'Audiences will be warned by the cinema if a film contains violent images.' },
        { frage: "My friend has been making animated films since he did an art degree. If my friend hadn't ...  ", antwort: "If my friend hadn't done an art degree, he wouldn’t have been making animated films since then." },
        { frage: "Girls aren't encouraged to become film directors by seeing films without female heroines. Girls might ...", antwort: 'Girls might be encouraged to become film directors if they saw films with female heroines.' }
      ]
    },
    {
      titel: 'Exercise 2',
      beschreibung: 'Put the expressions below in the correct order and use them to complete the sentences. There is one expression that you do not need:                              long, as, as / you, should, start / for, but / no, what, matter / unless / how, matter no / I had realized',
      aufgaben: [
        { frage: "[...] that the film was an adaptation of my favourite book, I wouldn't have gone to see it. ", antwort: 'Had I realized' },
        { frage: "[...] you understand that this isn't a film with a typical happy ending, you might enjoy it.  ", antwort: 'As long as' },
        { frage: "As a director concerned about moral and ethical issues, she won't make films about crime [...] the criminals are punished  ", antwort: 'unless' },
        { frage: "[...] the terrible ending, boring characters and lack of plot, I might have enjoyed it! ", antwort: 'But for' },
        { frage: "After seeing that film, I'll never watch science fiction again, [...] good the reviews are ", antwort: 'no matter how' },
      ]
    },

    {
      titel: 'Exercise 3',
      beschreibung: 'Complete the sentences with the following words: that, so that, as, while, even though, befor',
      aufgaben: [
        { frage: "I'm not looking for love [...] I believe love is an illusion.  ", antwort: 'as' },
        { frage: "It's true that some people never find love [...] they are beautiful and interesting.   ", antwort: 'even though' },
        { frage: "His proposal was so romantic [...] she couldn't say no, and they were married soon after.   ", antwort: 'that' },
        { frage: "Don't expect to find lasting love [...] you are still so young", antwort: 'while' },
        { frage: "People often spend money on clothes and shoes [...] they appear more attractive. ", antwort: 'so that' },
        { frage: "A fortune-teller recently told me that it wouldn't be long [...] I found true love. ", antwort: 'before' },
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