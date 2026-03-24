import { Component, Input } from '@angular/core';
import { ApiService } from 'src/app/service/api';

@Component({
  selector: 'app-file-download',
  templateUrl: './file-download.component.html',
  styleUrls: ['./file-download.component.scss'],
})
export class FileDownloadComponent{
//9850902c-35d1-46d8-9d0e-f211d15f56e7
  constructor(private api:ApiService) { }

  @Input() fileID:string="";
  getFile(){
    this.api.downloadFile(this.fileID).subscribe((blob)=>{
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
      window.URL.revokeObjectURL(url);
    })
  }

}
