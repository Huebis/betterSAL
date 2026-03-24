import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ApiService } from 'src/app/service/api';
import { FileDownloadComponent } from "../file-download/file-download.component";

export interface Item{
  fileID:string
}
@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.scss'],
  imports: [FileDownloadComponent],
})
export class FileUploadComponent{

  constructor(private api:ApiService) { }

  @Input() item:Item={fileID:""};
  @Output() change = new EventEmitter<void>();

  fileUploaded=false;

  onFileSelect(event: any, item:Item){
    let file = event.target.files[0];
    if (file){
      this.api.uploadFile(file).subscribe( v => {
        item.fileID = v.fileID;
        this.change.emit();
      }) 
    }
  }
  changeFile(){
    this.item.fileID="";

  }

}
