import { Injectable } from '@angular/core';
import {
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth';

@Injectable()
export class UuidInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const uuid = this.authService.getUuid();
    console.log("interceptor works")
    if (!uuid) {
      console.log("no uuid")
      return next.handle(req)
    };

    const cloned = req.clone({
      body: {...req.body,'token': uuid }
    });

    return next.handle(cloned);
  }
}
