import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'https://huebis.dev/betterSAL/api/';
  //private baseUrl = 'http://127.0.0.1:5000/betterSAL/api/';

  constructor(private http: HttpClient) {}


  sendRequest(data: Object,substring: string): Observable<any> {
    console.log(JSON.stringify(data))
    return this.http.post<any>(this.baseUrl+substring, data,{ headers: new HttpHeaders({'Content-Type':'application/json'})});
  }
  
}
