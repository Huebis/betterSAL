import { CommonModule } from '@angular/common';
import {Component, Input } from '@angular/core';

import { TimeDisplayComponent } from '../time-display/time-display.component';
import { IonIcon } from '@ionic/angular/standalone'; 
import { addIcons } from 'ionicons'; 
import { chevronDownOutline } from 'ionicons/icons';

@Component({
  selector: 'app-dropdown',
  templateUrl: './dropdown.component.html',
  styleUrls: ['./dropdown.component.scss'],
  imports: [CommonModule,IonIcon],
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
