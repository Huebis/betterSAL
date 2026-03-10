import { CommonModule } from '@angular/common';
import {Component, Input } from '@angular/core';


@Component({
  selector: 'app-dropdown',
  templateUrl: './dropdown.component.html',
  styleUrls: ['./dropdown.component.scss'],
  imports: [CommonModule],
})
export class DropdownComponent {
  @Input() headerItems:any={}
  @Input() items:Array<any>=[{

  }];
  @Input() headerTemplate:any;
  @Input() itemTemplate:any;

  isOpen: boolean = false;
  constructor() { }
  toggleDropdown() {
    this.isOpen = !this.isOpen;
  }
}
