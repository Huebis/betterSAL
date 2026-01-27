import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Files {
  constructor() {}
  downloadFile(fileId:string): Observable<Blob>{
    return this.api.sendRequest('/')
  }
 
  download(url: string): Observable<Blob> {
    return this.http.get(url, {
      responseType: 'blob'
    })
  }
}
