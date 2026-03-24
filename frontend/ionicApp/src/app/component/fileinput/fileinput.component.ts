import { Component, Input } from '@angular/core';
import { ApiService } from 'src/app/service/api';

@Component({
  selector: 'app-fileinput',
  templateUrl: './fileinput.component.html',
  styleUrls: ['./fileinput.component.scss'],
})
export class FileInputComponent{

  constructor(private api:ApiService) { }
  @Input() fileID:string="";
  
  getFile(){
    this.api.sendRequestGet({fileID:this.fileID},"getFileByFileID").subscribe( v => {
      console.log(v);
    })
  }

}
