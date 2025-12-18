import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:5000/';
  
  constructor(private http:HttpClient) {}
  setUrl(substring:string) {this.apiUrl=this.apiUrl+substring}

  sendData(body: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, body);
  }

  response: any;

  sendRequest(data:Object) {

    this.sendData(data).subscribe({
      next: (res) => this.response = res,
      error: (err) => console.error(err)
    });
    return this.response;
  }
}
