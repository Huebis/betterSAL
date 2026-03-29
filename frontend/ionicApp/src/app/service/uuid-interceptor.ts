//fügt bei jeder anfrage UUID hinzu (falls forhanden ansonst example UUID)

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
    console.log("interceptor works");
    let uuid = this.authService.getUuid();
    if (!uuid) {
      let tempUuid = "6bb28929-5385-405f-bd00-5b3f9666620b"
      const cloned = req.clone({
        headers: req.headers.set('token', tempUuid)
      });
      return next.handle(cloned);

    };

    const cloned = req.clone({
      headers: req.headers.set('token', uuid)
    });

    return next.handle(cloned);
  }
};
