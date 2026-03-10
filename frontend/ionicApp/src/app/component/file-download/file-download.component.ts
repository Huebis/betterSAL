import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-file-download',
  templateUrl: './file-download.component.html',
  styleUrls: ['./file-download.component.scss'],
})
export class FileDownloadComponent{

  constructor() { }

  @Input() link:string="";

}
