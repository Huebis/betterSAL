//Service um alle anfragen zu senden (Post, Get, uploadFile, downloadfile)
//fügt informationen hinzu und sendet and die BaseURL+ subpage



import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpHeaders, HttpParams } from '@angular/common/http';
import { catchError, Observable, of, switchMap, tap } from 'rxjs';
import { Router, RouterOutlet } from '@angular/router';


@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'https://huebis.dev/betterSAL/api/';
  //private baseUrl = 'http://127.0.0.1:5000/betterSAL/api/';

  constructor(private http: HttpClient, private router: Router) {}


  sendRequestPost(data: Object,substring: string): Observable<any> {
    console.log(data);
    return this.http.post<any>(this.baseUrl+substring, data,{ headers: new HttpHeaders({'Content-Type':'application/json'})});
  }
  sendRequestGet(data: any, substring: string): Observable<any> {
    let params = new HttpParams();
    console.log(data);
    for (let key in data){
      params=params.set(""+key, data[""+key] ? data[""+key] : "nothing");
    }
    return this.http.get<any>(this.baseUrl+substring,{params})
      .pipe(
        catchError((err) => {
          if (err.status===450){
            this.router.navigate(["/login"]);
          }
          console.log(err.status)
          return of();
        })
      );
  }
  uploadFile(file: any): Observable<any> {
    const fd = new FormData();
    fd.append('file', file);

    return this.http.post(this.baseUrl+"file", fd);
  }
  downloadFile(fileID:string): Observable<Blob> {
    return this.http.get(this.baseUrl+"file/" + fileID, {responseType: 'blob'})
  }
}
