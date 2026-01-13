import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private baseUrl = 'http://127.0.0.1:5000/';

  constructor(private http: HttpClient) {}

  // optional: dynamically append path
  setUrl(subpath: string) {
    if (!this.baseUrl.endsWith('/')) {
      this.baseUrl += '/';
    }
    this.baseUrl = this.baseUrl + subpath;
  }

  // send POST request
  sendData(body: any): Observable<any> {
    return this.http.post<any>(this.baseUrl, body);
  }

  // sendRequest now just returns Observable
  sendRequest(data: Object): Observable<any> {
    return this.sendData(data);
  }
}
