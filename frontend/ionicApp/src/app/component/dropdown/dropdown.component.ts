import { CommonModule } from '@angular/common';
import {Component, Input } from '@angular/core';

import { TimeDisplayComponent } from '../time-display/time-display.component';
import { addIcons } from 'ionicons'; 
import { chevronDownOutline } from 'ionicons/icons';

import {IonIcon, IonHeader,IonToolbar,IonTitle, IonButtons, IonContent, IonButton, IonInput,IonCheckbox} from "@ionic/angular/standalone";
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dropdown',
  templateUrl: './dropdown.component.html',
  styleUrls: ['./dropdown.component.scss'],
  standalone: true,
  imports: [CommonModule,IonIcon, IonHeader,IonToolbar,IonTitle, IonButtons, IonContent, IonButton, IonInput,IonCheckbox,FormsModule],
})
export class DropdownComponent {
  @Input() headerItems:any={}
  @Input() items:Array<any>=[{}];
  @Input() headerTemplate:any;
  @Input() itemTemplate:any;

  isOpen: boolean = false;
  constructor() { 
    addIcons({ chevronDownOutline });
  }
  toggleDropdown() {
    this.isOpen = !this.isOpen;
  }
}


