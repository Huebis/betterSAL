import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-fileinput',
  templateUrl: './fileinput.component.html',
  styleUrls: ['./fileinput.component.scss'],
})
export class FileInputComponent{

  constructor() { }
  @Input() link:string="";
}
