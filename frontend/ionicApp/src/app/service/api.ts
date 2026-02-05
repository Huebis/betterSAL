import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'https://huebis.dev/betterSAL/api/';
  //private baseUrl = 'http://127.0.0.1:5000/betterSAL/api/';

  constructor(private http: HttpClient) {}


  sendRequestPost(data: Object,substring: string): Observable<any> {
    console.log(JSON.stringify(data))
    return this.http.post<any>(this.baseUrl+substring, data,{ headers: new HttpHeaders({'Content-Type':'application/json'})});
  }
  sendRequestGet(data: any, substring: string): Observable<any> {
    let params = new HttpParams();
    console.log(data);
    for (let key in data){
      if (data[""+key]){
        params=params.set(""+key, data[""+key]);
      }
    }
    return this.http.get<any>(this.baseUrl+substring,{params});
  }
  
}
